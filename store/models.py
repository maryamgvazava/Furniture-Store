from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Product(models.Model):
    COLOR_CHOICES = [
        ('white', 'White'),
        ('black', 'Black'),
        ('brown', 'Brown'),
        ('gray', 'Gray'),
        ('beige', 'Beige'),
    ]
    
    MATERIAL_CHOICES = [
        ('wood', 'Wood'),
        ('metal', 'Metal'),
        ('glass', 'Glass'),
        ('leather', 'Leather'),
        ('textile', 'Textile'),
        ('plastic', 'Plastic'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, blank=True)
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'is_available']),
        ]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product.name} - Image"
    
    class Meta:
        ordering = ['-is_primary', 'created_at']


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_items(self):
        return self.items.count()
    
    def get_total_items_count(self):
        return sum(item.quantity for item in self.items.all())
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    class Meta:
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    
    def get_total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    class Meta:
        unique_together = ('cart', 'product')
        ordering = ['-added_at']


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import datetime
            import random
            dt = datetime.datetime.now()
            self.order_number = f"ORD{dt.year}{dt.month:02d}{dt.day:02d}{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.order_number}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['user', 'status']),
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_total_price(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.order_number}"
    
    class Meta:
        ordering = ['id']
