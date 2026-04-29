# Deployment Guide - Ngawasolutions Backend

## Docker Deployment (Recommended)

### Prerequisites
- Docker installed
- Docker Compose installed
- Neon PostgreSQL account with database credentials

### Step 1: Prepare Environment

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your Neon credentials:
```env
# Database Configuration (Neon PostgreSQL)
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=npg_YplWtR1ro8cy              # Your Neon password
DB_HOST=ep-blue-math-aigofdxp-pooler.c-4.us-east-1.aws.neon.tech  # Your Neon host
DB_PORT=5432
```

### Step 2: Build and Start

```bash
# Build Docker image and start containers
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f web
```

### Step 3: Verify Deployment

The services will automatically:
1. Create the database schema (migrations)
2. Create admin user (admin/Admin123.)
3. Seed default categories
4. Start the Gunicorn server

```bash
# Test the API
curl http://localhost:8000/api/categories/

# Expected response: JSON array of categories
```

### Step 4: Access Admin Panel

Navigate to: `http://localhost:8000/admin/`

**Credentials:**
- Username: `admin`
- Password: `Admin123.`

## Docker Compose Services

### Web Service (Django API)
- Port: 8000
- Command: Runs Django migrations, admin init, category seeding, then Gunicorn
- Health check: Checks API endpoint every 10 seconds

### DB Service (PostgreSQL - Optional)
- Port: 5432
- For local testing only
- Use Neon database for production

## Docker Commands Reference

```bash
# Start services in background
docker-compose up -d

# Rebuild and start
docker-compose up -d --build

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove volumes (database data)
docker-compose down -v

# View logs
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f web

# View specific service logs
docker-compose logs web

# Execute Django command in container
docker-compose exec web python manage.py <command>

# Access Django shell
docker-compose exec web python manage.py shell

# Create database backup
docker-compose exec db pg_dump -U postgres neondb > backup.sql

# Restart services
docker-compose restart

# Restart specific service
docker-compose restart web
```

## Managing the Django Application

```bash
# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Initialize admin user
docker-compose exec web python manage.py init_admin

# Seed categories
docker-compose exec web python manage.py seed_categories

# Create empty migration
docker-compose exec web python manage.py makemigrations

# Show migration status
docker-compose exec web python manage.py showmigrations

# Reset database
docker-compose exec web python manage.py migrate zero
```

## Configuration Changes

### Change Port
Edit `docker-compose.yml`:
```yaml
services:
  web:
    ports:
      - "8001:8000"  # Maps 8001 on host to 8000 in container
```

### Change Admin Credentials
Edit `.env`:
```env
ADMIN_USERNAME=myusername
ADMIN_PASSWORD=MyPassword123
ADMIN_EMAIL=admin@example.com
```

Then reinitialize:
```bash
docker-compose exec web python manage.py init_admin
```

### Update CORS Origins
Edit `.env`:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://example.com,https://app.example.com
```

No restart needed, takes effect immediately.

## Production Deployment Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Use strong `SECRET_KEY`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Configure proper `CORS_ALLOWED_ORIGINS`
- [ ] Use Neon PostgreSQL (not local Postgres)
- [ ] Set up SSL/TLS certificates (nginx)
- [ ] Use environment secrets management
- [ ] Configure backup strategy for database
- [ ] Set up monitoring/logging
- [ ] Configure reverse proxy (nginx)
- [ ] Set up automated restarts on failure

## Kubernetes Deployment

For Kubernetes, create ConfigMap for environment:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ngawasolutions-config
data:
  DEBUG: "False"
  ALLOWED_HOSTS: "api.example.com"
  CORS_ALLOWED_ORIGINS: "https://app.example.com"
```

Create Secret for sensitive data:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ngawasolutions-secrets
type: Opaque
stringData:
  SECRET_KEY: "your-secret-key"
  DB_PASSWORD: "your-neon-password"
```

## Troubleshooting

### Containers won't start
```bash
# Check logs
docker-compose logs web

# Rebuild
docker-compose down -v
docker-compose up -d --build
```

### Database connection error
1. Verify `.env` has correct Neon credentials
2. Check internet connectivity
3. Verify database isn't restricted by IP
4. Test connection:
```bash
docker-compose exec web psql postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME
```

### Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Admin user locked out
```bash
# Reinitialize with default credentials
docker-compose exec web python manage.py init_admin
```

### Static files not loading
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Database migrations stuck
```bash
# Show migration status
docker-compose exec web python manage.py showmigrations

# Reset to specific migration
docker-compose exec web python manage.py migrate products 0001
```

## Monitoring and Logging

### View application logs
```bash
docker-compose logs -f web
```

### View database logs
```bash
docker-compose logs -f db
```

### Monitor resource usage
```bash
docker stats
```

### Export logs
```bash
docker-compose logs web > app.log
docker-compose logs db > db.log
```

## Backup and Restore

### Backup Database
```bash
docker-compose exec db pg_dump -U postgres neondb > backup.sql
```

### Restore Database
```bash
docker-compose exec -T db psql -U postgres neondb < backup.sql
```

### Backup Volumes
```bash
docker run --rm -v ngawasolutions_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup.tar.gz /data
```

## Performance Tuning

### Increase Gunicorn Workers
Edit `docker-compose.yml`:
```yaml
command: sh -c "gunicorn --bind 0.0.0.0:8000 --workers 8 ngawasolutions.wsgi:application"
```

### Database Connection Pooling
Edit `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

### Enable Caching
Install redis:
```bash
docker-compose up -d redis
```

Configure in settings.py:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
```

## Health Checks

The web service includes a health check:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/api/categories/"]
  interval: 10s
  timeout: 5s
  retries: 5
```

Check health status:
```bash
docker-compose ps
```

## Rolling Updates

Update application code without downtime:
```bash
# Pull latest code
git pull origin main

# Rebuild
docker-compose build web

# Start new container
docker-compose up -d web

# Docker will stop old container after new one is healthy
```

## Security Best Practices

1. **Never commit secrets**
   - Use `.env` file (add to `.gitignore`)
   - Use `.env.example` for templates

2. **Non-root Docker user**
   - Already configured in Dockerfile

3. **Environment-based secrets**
   - Don't hardcode passwords
   - Use `.env` files

4. **CORS restrictions**
   - Only allow trusted origins
   - Don't use `*` in production

5. **Database security**
   - Use strong passwords
   - Restrict database access to app servers
   - Enable SSL/TLS for connections

6. **API security**
   - Implement rate limiting
   - Use HTTPS in production
   - Validate all inputs
   - Use admin authentication

## Scaling Strategy

### Horizontal Scaling
Use Docker Swarm or Kubernetes:
```bash
docker swarm init
docker stack deploy -c docker-compose.yml ngawasolutions
```

### Load Balancing
Configure Nginx in front:
```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://django;
    }
}
```

## Support

For deployment issues:
- Check logs: `docker-compose logs`
- Verify `.env` configuration
- Test database connectivity
- Check port availability

## Resources

- Docker Documentation: https://docs.docker.com
- Django Documentation: https://docs.djangoproject.com
- DRF Documentation: https://www.django-rest-framework.org
- Neon Documentation: https://neon.tech/docs
