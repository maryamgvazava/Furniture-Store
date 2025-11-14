# Furniture Store - Django E-commerce Platform

A complete Django-based online furniture store with REST API functionality. This project includes a full-featured e-commerce platform with product catalog, user management, shopping cart, and order processing.

## Features

- **User Management**: Custom user model with extended profile information
- **Product Catalog**: Browse furniture by categories with filtering options
- **Shopping Cart**: Add/remove items, view cart totals
- **Order Processing**: Complete order workflow from cart to delivery
- **REST API**: Full API implementation with Django REST Framework
- **Admin Interface**: Comprehensive Django admin for managing the store
- **Authentication**: Token-based authentication for API endpoints

## Tech Stack

- Django 5.2.8
- Django REST Framework 3.16.1
- SQLite Database
- Pillow for image handling
- Token Authentication

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd FurnitureStore
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create sample data (optional)**
```bash
python manage.py populate_db
```
This will create:
- Admin user: `admin` / `admin123`
- Test users: `user1`, `user2`, `user3` (password: `password123`)
- All 9 furniture categories
- 3-5 products per category
- Sample orders and cart items

6. **Run the development server**
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
FurnitureStore/
├── accounts/           # User management app
│   ├── models.py      # CustomUser model
│   └── admin.py       # User admin configuration
├── store/             # Main store app
│   ├── models.py      # Product, Category, Cart, Order models
│   └── admin.py       # Store admin configuration
├── api/               # REST API app
│   ├── serializers.py # DRF serializers
│   ├── views.py       # API views
│   └── urls.py        # API URL routing
├── media/             # User uploaded files
│   ├── categories/    # Category images
│   └── products/      # Product images
├── static/            # Static files (CSS, JS)
└── db.sqlite3         # SQLite database (included for assignment)
```

## Models

### CustomUser
- Extends Django's AbstractUser
- Additional fields: phone, address, birth_date
- Method: get_full_name()

### Category
- Fields: name, slug, description, image, is_active
- Pre-populated with 9 categories

### Product
- Fields: name, slug, category, description, price, stock, is_available, featured
- Color choices: white, black, brown, gray, beige
- Material choices: wood, metal, glass, leather, textile, plastic
- Support for multiple product images

### Cart & CartItem
- One-to-one relationship with user
- Methods: get_total_price(), get_total_items(), get_total_items_count()

### Order & OrderItem
- Status choices: pending, processing, shipped, delivered, canceled
- Auto-generated unique order numbers
- Static price snapshot at time of order

## API Endpoints

### Authentication
- `POST /api/register/` - User registration
- `POST /api/login/` - User login
- `GET /api/profile/` - Get/Update user profile (authenticated)

### Categories
- `GET /api/categories/` - List all categories
- `GET /api/categories/<id>/` - Get category details

### Products
- `GET /api/products/` - List all products (with filtering)
  - Query parameters: category, color, material, featured
- `GET /api/products/<id>/` - Get product details

### Cart
- `GET /api/cart/` - View cart (authenticated)
- `POST /api/cart/add/` - Add item to cart (authenticated)
- `POST /api/cart/remove/` - Remove item from cart (authenticated)

### Orders
- `GET /api/orders/` - List user orders (authenticated)
- `GET /api/orders/<id>/` - Get order details (authenticated)
- `POST /api/orders/create/` - Create order from cart (authenticated)

## Admin Interface

Access the admin interface at `http://127.0.0.1:8000/admin/`

Default credentials:
- Username: `admin`
- Password: `admin123`

### Admin Features
- **Category Management**: Add/edit categories with auto-generated slugs
- **Product Management**: Bulk edit prices/stock, inline image editing
- **User Management**: Search by phone/username, filter by address
- **Order Management**: Track order status, view order items
- **Cart Management**: Monitor user carts and items

## API Authentication

The API uses token authentication. To authenticate:

1. **Register or login to get token:**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "password123"}'
```

2. **Use token in subsequent requests:**
```bash
curl -X GET http://127.0.0.1:8000/api/cart/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Testing the API

### Using curl

**List all products:**
```bash
curl http://127.0.0.1:8000/api/products/
```

**Filter products by category:**
```bash
curl http://127.0.0.1:8000/api/products/?category=1
```

**Add item to cart (authenticated):**
```bash
curl -X POST http://127.0.0.1:8000/api/cart/add/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

### Using Python requests

```python
import requests

# Login
response = requests.post('http://127.0.0.1:8000/api/login/', 
    json={'username': 'user1', 'password': 'password123'})
token = response.json()['token']

# Get products
headers = {'Authorization': f'Token {token}'}
products = requests.get('http://127.0.0.1:8000/api/products/', headers=headers)
print(products.json())
```

## Sample Data

The project includes pre-populated data:

### Categories (9 total)
- Chair
- Sofa
- Table
- Wardrobe
- Bed
- Cabinet/Nightstand
- Shelf
- Armchair
- Outdoor Furniture

### Products
- 3-5 products per category
- Realistic pricing and stock levels
- Various colors and materials
- Featured products marked

### Users
- Admin: `admin` / `admin123`
- User1: `user1` / `password123`
- User2: `user2` / `password123`
- User3: `user3` / `password123`

## Development Notes

- The `db.sqlite3` file is included for assignment submission
- Media files are included with placeholder images
- CORS is configured for localhost:3000 and localhost:8000
- Debug mode is ON for development
- Static files are served in development mode

## Optional: Celery Integration

The project includes configuration for Celery (optional/advanced):
- Task: send_order_confirmation_email
- Task: update_order_status

To use Celery features, install Redis and run:
```bash
pip install celery redis
celery -A furniture_store worker --loglevel=info
```

## Security Notes

⚠️ **For Production Deployment:**
- Change SECRET_KEY in settings.py
- Set DEBUG = False
- Configure proper database (PostgreSQL recommended)
- Set up proper media file serving
- Configure ALLOWED_HOSTS
- Use environment variables for sensitive data
- Enable HTTPS
- Configure proper CORS settings

## License

This project is created for educational purposes as a final assignment.

## Support

For issues or questions, please contact the development team.