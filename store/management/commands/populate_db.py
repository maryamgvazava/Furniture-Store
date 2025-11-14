from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from decimal import Decimal
import random
from store.models import Category, Product, ProductImage, Cart, CartItem, Order, OrderItem

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample furniture data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate database...')
        
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@furniture.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                phone='+1234567890',
                address='123 Admin Street, Admin City, AC 12345'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created: admin / admin123'))
        
        # Create sample users
        users = []
        for i in range(1, 4):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    first_name=f'User{i}',
                    last_name=f'Test{i}',
                    phone=f'+123456789{i}',
                    address=f'{i}23 Test Street, Test City, TC 1234{i}'
                )
                users.append(user)
                # Create cart for user
                Cart.objects.get_or_create(user=user)
                self.stdout.write(self.style.SUCCESS(f'User created: {username} / password123'))
        
        # Categories data
        categories_data = [
            {
                'name': 'Chair',
                'description': 'Comfortable and stylish chairs for your home and office',
            },
            {
                'name': 'Sofa',
                'description': 'Luxurious sofas for your living room',
            },
            {
                'name': 'Table',
                'description': 'Dining tables, coffee tables, and work desks',
            },
            {
                'name': 'Wardrobe',
                'description': 'Spacious wardrobes for your bedroom',
            },
            {
                'name': 'Bed',
                'description': 'Comfortable beds for a good night\'s sleep',
            },
            {
                'name': 'Cabinet/Nightstand',
                'description': 'Storage cabinets and bedside nightstands',
            },
            {
                'name': 'Shelf',
                'description': 'Wall shelves and bookcases for storage and display',
            },
            {
                'name': 'Armchair',
                'description': 'Cozy armchairs for relaxation',
            },
            {
                'name': 'Outdoor Furniture',
                'description': 'Durable furniture for patios and gardens',
            },
        ]
        
        # Create categories
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=slugify(cat_data['name']),
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'is_active': True
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Category created: {category.name}'))
        
        # Products data for each category
        products_data = {
            'Chair': [
                {'name': 'Modern Office Chair', 'price': 299.99, 'stock': 25, 'color': 'black', 'material': 'leather'},
                {'name': 'Ergonomic Desk Chair', 'price': 449.99, 'stock': 15, 'color': 'gray', 'material': 'textile'},
                {'name': 'Dining Chair Set', 'price': 189.99, 'stock': 40, 'color': 'brown', 'material': 'wood'},
                {'name': 'Kitchen Bar Stool', 'price': 129.99, 'stock': 30, 'color': 'white', 'material': 'metal'},
                {'name': 'Gaming Chair Pro', 'price': 599.99, 'stock': 10, 'color': 'black', 'material': 'leather'},
            ],
            'Sofa': [
                {'name': 'L-Shaped Sectional Sofa', 'price': 1299.99, 'stock': 8, 'color': 'gray', 'material': 'textile'},
                {'name': '3-Seater Leather Sofa', 'price': 1899.99, 'stock': 5, 'color': 'brown', 'material': 'leather'},
                {'name': 'Modern Loveseat', 'price': 799.99, 'stock': 12, 'color': 'beige', 'material': 'textile'},
                {'name': 'Convertible Sofa Bed', 'price': 999.99, 'stock': 10, 'color': 'gray', 'material': 'textile'},
                {'name': 'Chesterfield Sofa', 'price': 2299.99, 'stock': 3, 'color': 'black', 'material': 'leather'},
            ],
            'Table': [
                {'name': 'Glass Dining Table', 'price': 899.99, 'stock': 7, 'color': 'black', 'material': 'glass'},
                {'name': 'Wooden Coffee Table', 'price': 399.99, 'stock': 20, 'color': 'brown', 'material': 'wood'},
                {'name': 'Adjustable Standing Desk', 'price': 599.99, 'stock': 15, 'color': 'white', 'material': 'metal'},
                {'name': 'Round Kitchen Table', 'price': 449.99, 'stock': 10, 'color': 'beige', 'material': 'wood'},
                {'name': 'Executive Office Desk', 'price': 1199.99, 'stock': 5, 'color': 'brown', 'material': 'wood'},
            ],
            'Wardrobe': [
                {'name': '3-Door Wardrobe', 'price': 999.99, 'stock': 8, 'color': 'white', 'material': 'wood'},
                {'name': 'Sliding Door Wardrobe', 'price': 1399.99, 'stock': 5, 'color': 'gray', 'material': 'wood'},
                {'name': 'Walk-in Closet System', 'price': 2499.99, 'stock': 3, 'color': 'beige', 'material': 'wood'},
                {'name': 'Kids Wardrobe', 'price': 599.99, 'stock': 12, 'color': 'white', 'material': 'plastic'},
            ],
            'Bed': [
                {'name': 'King Size Platform Bed', 'price': 1299.99, 'stock': 6, 'color': 'brown', 'material': 'wood'},
                {'name': 'Queen Storage Bed', 'price': 999.99, 'stock': 8, 'color': 'gray', 'material': 'wood'},
                {'name': 'Twin Bunk Bed', 'price': 799.99, 'stock': 10, 'color': 'white', 'material': 'metal'},
                {'name': 'Upholstered Bed Frame', 'price': 1499.99, 'stock': 4, 'color': 'beige', 'material': 'textile'},
            ],
            'Cabinet/Nightstand': [
                {'name': 'Bedside Table Set', 'price': 249.99, 'stock': 25, 'color': 'brown', 'material': 'wood'},
                {'name': 'Storage Cabinet', 'price': 399.99, 'stock': 15, 'color': 'white', 'material': 'wood'},
                {'name': 'Modern Nightstand', 'price': 179.99, 'stock': 30, 'color': 'black', 'material': 'metal'},
                {'name': 'Vintage Cabinet', 'price': 599.99, 'stock': 8, 'color': 'brown', 'material': 'wood'},
            ],
            'Shelf': [
                {'name': '5-Tier Bookshelf', 'price': 299.99, 'stock': 20, 'color': 'brown', 'material': 'wood'},
                {'name': 'Floating Wall Shelf', 'price': 79.99, 'stock': 50, 'color': 'white', 'material': 'wood'},
                {'name': 'Industrial Shelf Unit', 'price': 449.99, 'stock': 12, 'color': 'black', 'material': 'metal'},
                {'name': 'Corner Display Shelf', 'price': 199.99, 'stock': 18, 'color': 'beige', 'material': 'wood'},
            ],
            'Armchair': [
                {'name': 'Leather Recliner', 'price': 899.99, 'stock': 10, 'color': 'brown', 'material': 'leather'},
                {'name': 'Accent Armchair', 'price': 499.99, 'stock': 15, 'color': 'gray', 'material': 'textile'},
                {'name': 'Wingback Chair', 'price': 699.99, 'stock': 8, 'color': 'beige', 'material': 'textile'},
                {'name': 'Swivel Armchair', 'price': 599.99, 'stock': 12, 'color': 'black', 'material': 'leather'},
            ],
            'Outdoor Furniture': [
                {'name': 'Patio Dining Set', 'price': 1499.99, 'stock': 5, 'color': 'brown', 'material': 'wood'},
                {'name': 'Garden Lounge Chair', 'price': 299.99, 'stock': 20, 'color': 'white', 'material': 'plastic'},
                {'name': 'Outdoor Sofa Set', 'price': 1999.99, 'stock': 3, 'color': 'gray', 'material': 'metal'},
                {'name': 'Hammock with Stand', 'price': 399.99, 'stock': 10, 'color': 'beige', 'material': 'textile'},
            ],
        }
        
        # Create products
        all_products = []
        for category in categories:
            if category.name in products_data:
                for i, product_data in enumerate(products_data[category.name]):
                    product, created = Product.objects.get_or_create(
                        slug=slugify(product_data['name']),
                        defaults={
                            'name': product_data['name'],
                            'category': category,
                            'description': f"High-quality {product_data['name'].lower()} made from premium {product_data.get('material', 'materials')}. "
                                         f"Perfect for modern homes and offices. Features durable construction, elegant design, "
                                         f"and excellent comfort. Available in {product_data.get('color', 'multiple colors')} color.",
                            'price': Decimal(str(product_data['price'])),
                            'stock': product_data['stock'],
                            'is_available': True,
                            'featured': i < 2,  # First 2 products in each category are featured
                            'color': product_data.get('color', ''),
                            'material': product_data.get('material', ''),
                        }
                    )
                    all_products.append(product)
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Product created: {product.name}'))
        
        # Create sample orders for users
        if users:
            for user in users[:2]:  # Create orders for first 2 users
                # Create a completed order
                order = Order.objects.create(
                    user=user,
                    status='delivered',
                    total_amount=Decimal('0'),
                    shipping_address=user.address,
                    phone=user.phone,
                    notes='Sample delivered order'
                )
                
                # Add random products to order
                total = Decimal('0')
                selected_products = random.sample(all_products, min(3, len(all_products)))
                for product in selected_products:
                    quantity = random.randint(1, 3)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price
                    )
                    total += product.price * quantity
                
                order.total_amount = total
                order.save()
                self.stdout.write(self.style.SUCCESS(f'Order created for {user.username}'))
                
                # Add some items to cart
                cart = user.cart
                cart_products = random.sample(all_products, min(2, len(all_products)))
                for product in cart_products:
                    CartItem.objects.get_or_create(
                        cart=cart,
                        product=product,
                        defaults={'quantity': random.randint(1, 2)}
                    )
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))