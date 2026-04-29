# Ngawasolutions Backend - Documentation Index

Welcome to the Ngawasolutions product management backend! This guide helps you navigate all the documentation and get started quickly.

## Start Here

**New to this project?** Start with one of these:

1. **[QUICKSTART.md](./QUICKSTART.md)** ⚡
   - 5-minute setup with Docker
   - Basic curl examples
   - Admin panel access
   - Perfect for: Getting it running NOW

2. **[README.md](./README.md)** 📖
   - Complete feature overview
   - Full API endpoint reference
   - Installation methods
   - Perfect for: Understanding the system

3. **[BACKEND_SUMMARY.md](../BACKEND_SUMMARY.md)** 📋
   - High-level project overview
   - File structure summary
   - Key features at a glance
   - Perfect for: Project overview

## Detailed Guides

### Setup & Deployment
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Production deployment guide
  - Docker Compose setup
  - Configuration options
  - Performance tuning
  - Scaling strategies
  - Troubleshooting

- **[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)** - Technical details
  - File-by-file breakdown
  - Database schema
  - API endpoints
  - Customization guide

### Configuration
- **[.env.example](./.env.example)** - Environment template
- **[.env](./.env)** - Your actual configuration

### Source Code
Key files in the project:

**Models & Data:**
- `products/models.py` - Category and Product models

**REST API:**
- `products/views.py` - API endpoints
- `products/serializers.py` - Data serialization

**Admin Panel:**
- `products/admin.py` - Django admin configuration

**Configuration:**
- `ngawasolutions/settings.py` - Django settings
- `ngawasolutions/urls.py` - URL routing

**Docker:**
- `Dockerfile` - Docker image
- `docker-compose.yml` - Services orchestration
- `entrypoint.sh` - Container startup script

## Quick Reference

### Start the Backend

**Using Docker (Recommended):**
```bash
docker-compose up -d --build
```

**Using Python:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py init_admin
python manage.py seed_categories
python manage.py runserver
```

### Access Points

| Resource | URL |
|----------|-----|
| API | http://localhost:8000/api/ |
| Admin Panel | http://localhost:8000/admin/ |
| Categories Endpoint | http://localhost:8000/api/categories/ |
| Products Endpoint | http://localhost:8000/api/products/ |

### Admin Credentials

- **Username:** admin
- **Password:** Admin123.

### Database

- **Type:** PostgreSQL (Neon)
- **Connection:** See `.env` file
- **Migrations:** Run automatically on startup

## Common Tasks

### Add a Product
1. Go to http://localhost:8000/admin/
2. Click "Products" → "Add product"
3. Fill in details and select category
4. Click "Save"

### Add a Category
1. Go to http://localhost:8000/admin/
2. Click "Categories" → "Add category"
3. Enter name and description
4. Click "Save"

### Change Admin Password
```bash
docker-compose exec web python manage.py init_admin
```

### Reset Categories
```bash
docker-compose exec web python manage.py seed_categories
```

### Access Database Shell
```bash
docker-compose exec web python manage.py shell
```

### View Logs
```bash
docker-compose logs -f web
```

## API Quick Examples

### Get all categories
```bash
curl http://localhost:8000/api/categories/
```

### Get all products
```bash
curl http://localhost:8000/api/products/
```

### Get products in category
```bash
curl http://localhost:8000/api/products/by_category/
```

### Filter products by category
```bash
curl http://localhost:8000/api/products/?category_id=1
```

## File Navigation

```
backend/
├── QUICKSTART.md              ← Start here!
├── README.md                  ← Full documentation
├── DEPLOYMENT.md              ← Deployment guide
├── PROJECT_STRUCTURE.md       ← Technical details
├── INDEX.md                   ← This file
│
├── ngawasolutions/
│   ├── settings.py            ← Django config
│   ├── urls.py                ← URL routing
│   └── wsgi.py                ← Production config
│
├── products/
│   ├── models.py              ← Data models
│   ├── views.py               ← REST endpoints
│   ├── serializers.py         ← Data serialization
│   ├── admin.py               ← Admin interface
│   └── management/commands/
│       ├── init_admin.py      ← Create admin user
│       └── seed_categories.py ← Create default categories
│
├── manage.py                  ← Django CLI
├── requirements.txt           ← Dependencies
├── Dockerfile                 ← Docker image
├── docker-compose.yml         ← Services config
├── entrypoint.sh              ← Startup script
├── .env                       ← Configuration
└── .env.example               ← Config template
```

## Troubleshooting Guide

**Container won't start?**
- Check logs: `docker-compose logs web`
- See DEPLOYMENT.md → Troubleshooting

**Can't connect to database?**
- Verify `.env` credentials
- Check internet connection for Neon
- See DEPLOYMENT.md → Database Connection Error

**Admin panel not accessible?**
- Check services: `docker-compose ps`
- Try: `docker-compose restart web`

**API returning 404?**
- Verify URL: `http://localhost:8000/api/categories/`
- Check services running: `docker-compose ps`

**Forgot admin password?**
- Run: `docker-compose exec web python manage.py init_admin`

See DEPLOYMENT.md for more troubleshooting help.

## Customization

### Change Default Categories
Edit `products/management/commands/seed_categories.py`

### Change Admin Credentials
Edit `products/management/commands/init_admin.py`

### Add New Fields to Product
1. Update `products/models.py`
2. Run: `python manage.py makemigrations`
3. Run: `python manage.py migrate`
4. Update `products/serializers.py`
5. Update `products/admin.py`

### Change CORS Origins
Edit `.env`:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://myapp.com
```

## Performance Tips

- Endpoints support pagination (20 items/page)
- Use category_id query parameter to filter
- Use `/active/` endpoint for faster active products query
- Database indexes are optimized

## Security Reminders

✓ `.env` contains secrets - don't commit to git
✓ Change `SECRET_KEY` for production
✓ Only expose admin panel to trusted IPs
✓ Use HTTPS in production
✓ Keep Django updated

## Integration with React Frontend

1. Install axios or fetch API
2. Use base URL: `http://localhost:8000/api/`
3. CORS is pre-configured for `http://localhost:3000`
4. Example fetch:
```javascript
fetch('http://localhost:8000/api/products/')
  .then(res => res.json())
  .then(data => console.log(data))
```

See README.md for full API endpoint list.

## Docker Commands Summary

```bash
# Start
docker-compose up -d --build

# Stop
docker-compose down

# Logs
docker-compose logs -f web

# Execute command
docker-compose exec web python manage.py <command>

# Reset
docker-compose down -v
docker-compose up -d --build
```

## Getting Help

1. **Check documentation** - Start with README.md
2. **Search troubleshooting** - See DEPLOYMENT.md
3. **Check logs** - Run `docker-compose logs -f web`
4. **Test manually** - Use curl to test endpoints

## Project Info

- **Name:** Ngawasolutions
- **Type:** Django REST API
- **Database:** PostgreSQL (Neon)
- **Frontend:** React (your part)
- **Deployment:** Docker & Docker Compose
- **Status:** Production ready!

## What's Next?

1. ✓ Backend is ready
2. Go to http://localhost:8000/admin/ and add some products
3. Test API with curl or Postman
4. Build your React frontend
5. Connect to `http://localhost:8000/api/`

---

**Document Last Updated:** 2024-04-29
**Version:** 1.0
**Status:** Ready for Production

Questions? Check the README.md or DEPLOYMENT.md!
