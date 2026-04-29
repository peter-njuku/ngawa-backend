# Quick Start Guide - Ngawasolutions Backend

## Docker Deployment (Recommended)

The fastest way to get your backend running:

```bash
# 1. Navigate to backend directory
cd backend

# 2. Run with Docker Compose
docker-compose up -d --build

# 3. Wait for containers to start (about 30 seconds)

# 4. Access the API
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
  - Username: admin
  - Password: Admin123.
```

## Local Development

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy .env file
cp .env.example .env

# 5. Update .env with your Neon database credentials
# Edit: DB_HOST, DB_PASSWORD

# 6. Run migrations
python manage.py migrate

# 7. Initialize admin user
python manage.py init_admin

# 8. Seed categories
python manage.py seed_categories

# 9. Start server
python manage.py runserver
```

## Testing the API

### Get all categories
```bash
curl http://localhost:8000/api/categories/
```

### Get all products
```bash
curl http://localhost:8000/api/products/
```

### Get products by category
```bash
curl http://localhost:8000/api/products/?category_id=1
```

### Get products grouped by category
```bash
curl http://localhost:8000/api/products/by_category/
```

## Admin Panel

Access at: `http://localhost:8000/admin/`

**Default Login:**
- Username: `admin`
- Password: `Admin123.`

From here you can:
- Add new products
- Manage categories
- View all data
- Manage admin users

## API Documentation

Full API endpoints documented in `README.md`.

Quick reference:
- `GET /api/categories/` - List categories
- `GET /api/products/` - List products
- `GET /api/products/by_category/` - Products grouped by category
- `GET /api/products/active/` - Active products only

## Troubleshooting

### Port 8000 already in use?
Edit `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change to any free port
```

### Can't connect to database?
- Check `.env` has correct Neon credentials
- Verify internet connection for Neon database
- Check database password in `.env`

### Admin password not working?
Reset it:
```bash
python manage.py init_admin
```

### Need to reset everything?
```bash
# Docker
docker-compose down -v
docker-compose up -d --build

# Local
rm db.sqlite3
python manage.py migrate
python manage.py init_admin
python manage.py seed_categories
```

## Environment Variables

Key settings in `.env`:
- `DEBUG=False` - Set to True for local development
- `DB_HOST` - Your Neon database host
- `DB_PASSWORD` - Your Neon password
- `CORS_ALLOWED_ORIGINS` - Update for your frontend URL

## Next Steps

1. Update CORS_ALLOWED_ORIGINS in `.env` with your React frontend URL
2. Test API endpoints with curl or Postman
3. Integrate with React frontend
4. Add your own products via admin panel or API

For detailed documentation, see `README.md`.
