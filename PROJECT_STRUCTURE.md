# Ngawasolutions Backend - Project Structure

## Complete Directory Layout

```
backend/
│
├── ngawasolutions/                          # Main Django project
│   ├── __init__.py
│   ├── settings.py                          # Django configuration
│   ├── urls.py                              # URL routing
│   └── wsgi.py                              # WSGI for production
│
├── products/                                # Products app
│   ├── migrations/                          # Database migrations
│   │   ├── __init__.py
│   │   └── 0001_initial.py                  # Initial schema migration
│   ├── management/                          # Custom commands
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       ├── init_admin.py                # Creates/updates admin user
│   │       └── seed_categories.py           # Seeds default categories
│   ├── __init__.py
│   ├── admin.py                             # Django admin configuration
│   ├── apps.py                              # App configuration
│   ├── models.py                            # Category & Product models
│   ├── serializers.py                       # DRF serializers
│   └── views.py                             # API viewsets
│
├── manage.py                                # Django CLI entry point
├── requirements.txt                         # Python dependencies
├── Dockerfile                               # Docker image
├── docker-compose.yml                       # Docker composition
├── entrypoint.sh                            # Container startup script
│
├── .env                                     # Environment variables (with credentials)
├── .env.example                             # Example env template
├── .dockerignore                            # Files to exclude from Docker
├── .gitignore                               # Git ignore rules
│
├── README.md                                # Full documentation
├── QUICKSTART.md                            # Quick start guide
└── PROJECT_STRUCTURE.md                     # This file
```

## File Descriptions

### Core Django Files

**ngawasolutions/settings.py**
- Django configuration
- Database settings pointing to Neon PostgreSQL
- REST Framework configuration
- CORS configuration for React frontend
- Static files configuration

**ngawasolutions/urls.py**
- API routes registration
- Admin panel route
- REST Framework authentication route

**ngawasolutions/wsgi.py**
- WSGI application for production servers

### Products App

**products/models.py**
- `Category`: Product categories (Desktops, Laptops, Printers, Accessories)
- `Product`: Individual products linked to categories
- Both models have timestamps (created_at, updated_at)
- Product has stock, price, and active status

**products/serializers.py**
- `CategorySerializer`: For Category CRUD operations
- `ProductSerializer`: For Product CRUD operations
- Include related data (category name for products)

**products/views.py**
- `CategoryViewSet`: REST endpoints for categories
  - GET: Anyone can access
  - POST/PUT/DELETE: Admin only
  - Custom action: Get products in category
- `ProductViewSet`: REST endpoints for products
  - GET: Anyone can access
  - POST/PUT/DELETE: Admin only
  - Custom actions: Group by category, get active only

**products/admin.py**
- Customized Django admin for categories and products
- List views with filters and search
- Editable fields with organizing fieldsets

**products/management/commands/init_admin.py**
- Creates default admin user if doesn't exist
- Updates password if user exists
- Default: admin / Admin123.

**products/management/commands/seed_categories.py**
- Seeds 4 default categories:
  1. Desktops
  2. Laptops
  3. Printers
  4. Accessories

### Docker Files

**Dockerfile**
- Python 3.11 slim image
- Installs PostgreSQL client and dependencies
- Creates non-root user for security
- Runs Gunicorn on port 8000

**docker-compose.yml**
- Web service: Django application
- DB service: PostgreSQL database (optional)
- Volumes for persistence
- Health checks for both services
- Network isolation
- Auto-runs migrations and seeding on start

**entrypoint.sh**
- Runs migrations
- Initializes admin user
- Seeds categories
- Starts Gunicorn

### Configuration Files

**.env**
- Neon PostgreSQL credentials
- Django secret key
- Debug flag
- CORS origins
- Admin user credentials

**.env.example**
- Template for environment setup
- All variables documented

**.gitignore**
- Python cache and packages
- Virtual environments
- IDE settings
- Log files
- Database files

**.dockerignore**
- Excludes unnecessary files from Docker image

### Documentation

**README.md**
- Complete feature documentation
- Installation instructions (local and Docker)
- API endpoint reference
- Environment variable reference
- Troubleshooting guide
- Production deployment tips

**QUICKSTART.md**
- Fast setup guide
- Basic curl examples
- Troubleshooting quick fixes

**PROJECT_STRUCTURE.md**
- This file
- Detailed file descriptions

## API Endpoints Summary

### Categories
```
GET    /api/categories/              # List all
GET    /api/categories/{id}/         # Detail
GET    /api/categories/{id}/products/ # Category products
POST   /api/categories/              # Create (admin)
PUT    /api/categories/{id}/         # Update (admin)
DELETE /api/categories/{id}/         # Delete (admin)
```

### Products
```
GET    /api/products/                     # List all
GET    /api/products/?category_id={id}   # Filter by category
GET    /api/products/{id}/                # Detail
GET    /api/products/by_category/         # Grouped by category
GET    /api/products/active/              # Active only
POST   /api/products/                     # Create (admin)
PUT    /api/products/{id}/                # Update (admin)
DELETE /api/products/{id}/                # Delete (admin)
```

## Default Categories

The system automatically creates these categories:

1. **Desktops** - Desktop computers and systems
2. **Laptops** - Laptop computers and portable devices
3. **Printers** - Printers and printing devices
4. **Accessories** - Computer accessories and peripherals

## Database Schema

### Category Table
- `id` (BigAutoField, Primary Key)
- `name` (CharField, unique)
- `description` (TextField, optional)
- `created_at` (DateTimeField)
- `updated_at` (DateTimeField)

### Product Table
- `id` (BigAutoField, Primary Key)
- `name` (CharField)
- `description` (TextField, optional)
- `price` (DecimalField)
- `category_id` (ForeignKey → Category, PROTECT on delete)
- `stock` (IntegerField, default 0)
- `is_active` (BooleanField, default True)
- `created_at` (DateTimeField)
- `updated_at` (DateTimeField)

### Index
- `(category_id, is_active)` - For fast filtering of active products by category

## Deployment Instructions

### Docker Compose (Production-Ready)
```bash
# Build and start
docker-compose up -d --build

# View logs
docker-compose logs -f web

# Stop
docker-compose down
```

### Manual Deployment
```bash
# Install
pip install -r requirements.txt

# Setup
python manage.py migrate
python manage.py init_admin
python manage.py seed_categories

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 ngawasolutions.wsgi:application
```

## Security Considerations

✓ Non-root user in Docker
✓ Environment-based secrets (not in code)
✓ CORS configuration for specific origins
✓ Admin-only write operations
✓ PostgreSQL on-delete protection
✓ Password hashing via Django auth
✓ CSRF protection enabled

## Performance Features

✓ Database indexes on frequently filtered fields
✓ Select related queries for efficient joins
✓ Pagination support (20 items per page)
✓ Gunicorn with 4 workers
✓ Health checks in Docker

## Integration Points

The backend is designed to integrate with a React frontend:

1. **API Base URL**: `http://localhost:8000/api/`
2. **CORS Enabled**: Pre-configured for React at `http://localhost:3000`
3. **JSON Responses**: All endpoints return JSON
4. **Authentication**: Session-based (can be extended with tokens)
5. **Pagination**: Integrated in REST framework

## Development Workflow

1. Make changes to models/views
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Test endpoints with curl/Postman
5. Commit changes

## Customization

To add a new field to Product:
```python
# 1. Update models.py
# 2. Create migration: python manage.py makemigrations
# 3. Update serializers.py
# 4. Update admin.py (fieldsets)
# 5. Apply migration: python manage.py migrate
```

To add custom API actions:
```python
# In views.py viewset, use @action decorator
@action(detail=False, methods=['get'])
def custom_action(self, request):
    # Your logic here
    return Response(data)
```
