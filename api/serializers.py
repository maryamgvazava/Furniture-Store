from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from accounts.models import CustomUser
from store.models import Category, Product, ProductImage, Cart, CartItem, Order, OrderItem


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'address', 'birth_date']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name', 'phone', 'address', 'birth_date']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        Cart.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                data['user'] = user
            else:
                raise serializers.ValidationError('Invalid credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        return data


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active', 'product_count', 'created_at']

    def get_product_count(self, obj):
        return obj.products.filter(is_available=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'category_name', 'price', 'stock', 'is_available', 
                 'featured', 'color', 'material', 'primary_image']

    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            request = self.context.get('request')
            if request and primary.image:
                return request.build_absolute_uri(primary.image.url)
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'description', 'price', 'stock', 
                 'is_available', 'featured', 'color', 'material', 'in_stock', 'images', 
                 'created_at', 'updated_at']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.DecimalField(source='get_total_price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price', 'added_at']

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(pk=value, is_available=True)
            if product.stock < 1:
                raise serializers.ValidationError("Product is out of stock.")
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or unavailable.")
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(source='get_total_price', max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(source='get_total_items', read_only=True)
    total_items_count = serializers.IntegerField(source='get_total_items_count', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'total_items', 'total_items_count', 'updated_at']
        read_only_fields = ['user']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.DecimalField(source='get_total_price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'total_price']
        read_only_fields = ['price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user', 'status', 'total_amount', 'shipping_address', 
                 'phone', 'notes', 'items', 'created_at', 'updated_at']
        read_only_fields = ['order_number', 'user', 'total_amount']


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['shipping_address', 'phone', 'notes']

    def validate(self, data):
        request = self.context.get('request')
        if not request.user.cart.items.exists():
            raise serializers.ValidationError("Your cart is empty.")
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        cart = user.cart
        
        # Calculate total amount
        total_amount = cart.get_total_price()
        
        # Create order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            **validated_data
        )
        
        # Create order items from cart items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Update product stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart.items.all().delete()
        
        return order