from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse

from accounts.models import CustomUser
from store.models import Category, Product, Cart, CartItem, Order
from .serializers import (
    CustomUserSerializer, UserRegistrationSerializer, LoginSerializer,
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    CartSerializer, CartItemSerializer, OrderSerializer, CreateOrderSerializer
)


# API Root View
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_root(request):
    return Response({
        'message': 'Welcome to Furniture Store API',
        'endpoints': {
            'authentication': {
                'register': request.build_absolute_uri('/api/register/'),
                'login': request.build_absolute_uri('/api/login/'),
                'profile': request.build_absolute_uri('/api/profile/'),
            },
            'categories': {
                'list': request.build_absolute_uri('/api/categories/'),
                'detail': request.build_absolute_uri('/api/categories/<id>/'),
            },
            'products': {
                'list': request.build_absolute_uri('/api/products/'),
                'detail': request.build_absolute_uri('/api/products/<id>/'),
            },
            'cart': {
                'view': request.build_absolute_uri('/api/cart/'),
                'add': request.build_absolute_uri('/api/cart/add/'),
                'remove': request.build_absolute_uri('/api/cart/remove/'),
            },
            'orders': {
                'list': request.build_absolute_uri('/api/orders/'),
                'detail': request.build_absolute_uri('/api/orders/<id>/'),
                'create': request.build_absolute_uri('/api/orders/create/'),
            }
        },
        'authentication_note': 'Use Token authentication for protected endpoints. Add "Authorization: Token <your_token>" header.',
    })


# User Authentication Views
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': CustomUserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': CustomUserSerializer(user).data,
            'token': token.key
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# Category Views
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


# Product Views
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'color', 'material', 'featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]


# Cart Views
class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    if not product_id:
        return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=product_id, is_available=True)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found or unavailable'}, status=status.HTTP_404_NOT_FOUND)

    if product.stock < quantity:
        return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def remove_from_cart(request):
    product_id = request.data.get('product_id')
    
    if not product_id:
        return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart = request.user.cart
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not in cart'}, status=status.HTTP_404_NOT_FOUND)


# Order Views
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CreateOrderView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
