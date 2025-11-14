from django.urls import path
from .views import (
    api_root,
    RegisterView, LoginView, ProfileView,
    CategoryListView, CategoryDetailView,
    ProductListView, ProductDetailView,
    CartView, add_to_cart, remove_from_cart,
    OrderListView, OrderDetailView, CreateOrderView
)

app_name = 'api'

urlpatterns = [
    # API Root
    path('', api_root, name='api-root'),
    
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Products
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Cart
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', add_to_cart, name='add-to-cart'),
    path('cart/remove/', remove_from_cart, name='remove-from-cart'),
    
    # Orders
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/create/', CreateOrderView.as_view(), name='create-order'),
]