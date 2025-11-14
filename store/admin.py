from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Cart, CartItem, Order, OrderItem


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_primary']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available', 'featured', 'created_at']
    list_filter = ['category', 'is_available', 'featured', 'color', 'material', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_available', 'featured']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductImageInline]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing and Stock', {
            'fields': ('price', 'stock', 'is_available', 'featured')
        }),
        ('Additional Details', {
            'fields': ('color', 'material')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['product', 'quantity', 'get_total_price']
    readonly_fields = ['get_total_price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_items_count', 'get_total_price', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username', 'user__email']
    inlines = [CartItemInline]
    readonly_fields = ['get_total_price', 'get_total_items', 'get_total_items_count']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product', 'quantity', 'price', 'get_total_price']
    readonly_fields = ['get_total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['order_number', 'user__username', 'user__email', 'phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'total_amount')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'phone')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def has_delete_permission(self, request, obj=None):
        if obj and obj.status in ['processing', 'shipped', 'delivered']:
            return False
        return super().has_delete_permission(request, obj)
