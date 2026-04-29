# Ngawasolutions Product Management API

A Django REST Framework backend for managing products and categories. This API provides endpoints for product management with an admin panel for authorized users.

## Features

- **Product Management**: Create, read, update, and delete products
- **Category Management**: Manage product categories (Desktops, Laptops, Printers, Accessories)
- **Admin Panel**: Django admin interface at `/admin/` with default credentials
- **REST API**: Full RESTful API for frontend integration
- **CORS Support**: Pre-configured for React frontend integration
- **Docker Support**: Complete Docker and docker-compose setup for easy deployment

## Technology Stack

- Python 3.11
- Django 4.2
- Django REST Framework 3.14
- PostgreSQL (Neon)
- Gunicorn
- Docker

## Project Structure

```
backend/
├── ngawasolutions/          # Main Django project
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── __init__.py
├── products/                # Products app
│   ├── models.py            # Category and Product models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API viewsets
│   ├── admin.py             # Admin configuration
│   ├── management/
│   │   └── commands/
│   │       ├── init_admin.py        # Initialize admin user
│   │       └── seed_categories.py   # Seed default categories
│   └── __init__.py
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker compose setup
├── .env                    # Environment variables
├── .env.example            # Example environment file
└── README.md              # This file
```

## Installation & Setup

### Option 1: Local Development

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Neon database credentials
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Initialize admin user**
   ```bash
   python manage.py init_admin
   # Default: admin / Admin123.
   ```

7. **Seed default categories**
   ```bash
   python manage.py seed_categories
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000/api/`

### Option 2: Docker Deployment (Recommended)

1. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Neon database credentials
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d --build
   ```

   The API will be available at `http://localhost:8000/api/`

3. **Initialize database** (if not auto-initialized)
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py init_admin
   docker-compose exec web python manage.py seed_categories
   ```

## API Endpoints

### Categories

- `GET /api/categories/` - List all categories
- `GET /api/categories/{id}/` - Retrieve category details
- `GET /api/categories/{id}/products/` - Get products in a category
- `POST /api/categories/` - Create category (Admin only)
- `PUT /api/categories/{id}/` - Update category (Admin only)
- `DELETE /api/categories/{id}/` - Delete category (Admin only)

### Products

- `GET /api/products/` - List all products
- `GET /api/products/?category_id={id}` - Filter products by category
- `GET /api/products/{id}/` - Retrieve product details
- `GET /api/products/by_category/` - Products grouped by category
- `GET /api/products/active/` - Get active products only
- `POST /api/products/` - Create product (Admin only)
- `PUT /api/products/{id}/` - Update product (Admin only)
- `DELETE /api/products/{id}/` - Delete product (Admin only)

## Admin Panel

Access the Django admin panel at:
```
http://localhost:8000/admin/
```

**Default Credentials:**
- Username: `admin`
- Password: `Admin123.`

From the admin panel, you can:
- Create and manage product categories
- Add, edit, and delete products
- View product statistics
- Manage admin users

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Django debug mode | `False` |
| `SECRET_KEY` | Django secret key | Required for production |
| `ALLOWED_HOSTS` | Allowed host domains | `localhost,127.0.0.1` |
| `DB_NAME` | Database name | `neondb` |
| `DB_USER` | Database user | `neondb_owner` |
| `DB_PASSWORD` | Database password | Required |
| `DB_HOST` | Database host | Required |
| `DB_PORT` | Database port | `5432` |
| `CORS_ALLOWED_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |

## Default Categories

The system comes with 4 pre-defined categories:
1. **Desktops** - Desktop computers and systems
2. **Laptops** - Laptop computers and portable devices
3. **Printers** - Printers and printing devices
4. **Accessories** - Computer accessories and peripherals

## API Response Examples

### List Products
```bash
curl http://localhost:8000/api/products/
```

Response:
```json
[
  {
    "id": 1,
    "name": "Dell XPS 13",
    "description": "High-performance laptop",
    "price": "999.99",
    "category": 2,
    "category_name": "Laptops",
    "stock": 50,
    "is_active": true,
    "created_at": "2024-04-29T10:30:00Z",
    "updated_at": "2024-04-29T10:30:00Z"
  }
]
```

### Filter by Category
```bash
curl http://localhost:8000/api/products/?category_id=2
```

### Get Products by Category
```bash
curl http://localhost:8000/api/products/by_category/
```

Response:
```json
{
  "Laptops": [
    {
      "id": 1,
      "name": "Dell XPS 13",
      ...
    }
  ],
  "Desktops": [],
  "Printers": [],
  "Accessories": []
}
```

## Authentication

The API uses token-based authentication for admin operations:

1. Obtain a token (implement if needed)
2. Include the token in the `Authorization` header
3. Only admin users can create, update, or delete products/categories

## Docker Commands

```bash
# Build and start containers
docker-compose up -d --build

# Stop containers
docker-compose down

# View logs
docker-compose logs -f web

# Execute Django commands
docker-compose exec web python manage.py <command>

# Access Django shell
docker-compose exec web python manage.py shell

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## CORS Configuration

The backend is pre-configured to accept requests from:
- `http://localhost:3000` (React frontend)
- `http://127.0.0.1:3000`
- `http://localhost:8000`

Modify `CORS_ALLOWED_ORIGINS` in `.env` to add more origins.

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Use a strong `SECRET_KEY`
3. Update `ALLOWED_HOSTS` with your domain
4. Use a production database (Neon)
5. Configure proper CORS origins
6. Use environment-based secrets management
7. Set up SSL/TLS certificates
8. Use a production web server (Gunicorn + Nginx)

## Troubleshooting

### Database Connection Issues
- Verify Neon credentials in `.env`
- Check database host is accessible
- Ensure SSL mode is enabled for Neon connections

### Admin User Not Created
```bash
python manage.py init_admin
```

### Categories Not Seeded
```bash
python manage.py seed_categories
```

### Port Already in Use
Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change to any available port
```

## Support

For issues or questions, contact: admin@ngawasolutions.com

## License

MIT License - feel free to use this project for your needs.
