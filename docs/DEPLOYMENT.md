# Deployment Guide

## Prerequisites

- Production server (AWS, DigitalOcean, Heroku, etc.)
- Domain name
- SSL certificate
- PostgreSQL database
- Environment variables configured

## Deploying Backend

### Step 1: Prepare Backend Code

1. **Update configuration for production:**

```python
# backend/config.py
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 86400
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
```

2. **Update .env for production:**

```bash
FLASK_ENV=production
SECRET_KEY=generate-secure-random-string
DATABASE_URL=postgresql://user:password@db-server/cake_bakery
CORS_ORIGINS=https://yourdomain.com
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
```

3. **Add production requirements:**

```bash
# additional requirements-prod.txt
gunicorn==21.2.0
psycopg2-binary==2.9.9
redis==5.0.0
python-dotenv==1.0.0
```

### Step 2: Set Up Database (PostgreSQL)

```bash
# On server
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE cake_bakery;
CREATE USER bakery_user WITH PASSWORD 'strong-password';
ALTER ROLE bakery_user SET client_encoding TO 'utf8';
ALTER ROLE bakery_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE bakery_user SET default_transaction_deferrable TO on;
ALTER ROLE bakery_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cake_bakery TO bakery_user;
\q
```

### Step 3: Deploy to Linux Server

#### Option A: Manual Deployment

1. **SSH into server:**
```bash
ssh ubuntu@server-ip
```

2. **Install dependencies:**
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv nginx supervisor postgresql

pip3 install --upgrade pip
```

3. **Clone repository:**
```bash
cd /var/www
git clone https://github.com/yourusername/cake-bakery.git
cd cake-bakery/backend
```

4. **Set up virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with production values
nano .env
```

6. **Initialize database:**
```bash
python app.py
# This will create tables
```

7. **Test with Gunicorn:**
```bash
gunicorn -w 4 -b 127.0.0.1:8000 app:app
```

8. **Configure Supervisor:**

```bash
# Create supervisor config
sudo nano /etc/supervisor/conf.d/cake-bakery.conf

[program:cake-bakery]
directory=/var/www/cake-bakery/backend
command=/var/www/cake-bakery/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/cake-bakery.err.log
stdout_logfile=/var/log/cake-bakery.out.log
```

9. **Start Supervisor:**
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start cake-bakery
```

10. **Configure Nginx:**

```bash
# Create nginx config
sudo nano /etc/nginx/sites-available/cake-bakery

upstream cake_bakery {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://cake_bakery;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /var/www/cake-bakery/backend/static/;
    }
}
```

11. **Enable Nginx site:**
```bash
sudo ln -s /etc/nginx/sites-available/cake-bakery /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Option B: Docker Deployment

1. **Create Dockerfile:**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend .

# Run gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

2. **Build and push:**
```bash
docker build -t cake-bakery-backend:latest .
docker run -p 5000:5000 --env-file .env cake-bakery-backend:latest
```

#### Option C: Heroku Deployment

1. **Create Procfile:**
```
web: gunicorn app:app
```

2. **Create runtime.txt:**
```
python-3.10.0
```

3. **Deploy:**
```bash
heroku login
heroku create cake-bakery-app
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set FLASK_ENV=production
heroku config:set OPENAI_API_KEY=sk-...
git push heroku main
```

### Step 4: Enable HTTPS

```bash
# Install Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d yourdomain.com

# Auto-renew
sudo systemctl enable certbot.timer
```

---

## Deploying Frontend

### Step 1: Build Production Bundle

```bash
cd frontend
npm run build

# This creates dist/ folder with optimized code
```

### Step 2: Deploy to CDN/Static Host

#### Option A: Netlify

1. **Install Netlify CLI:**
```bash
npm install -g netlify-cli
```

2. **Deploy:**
```bash
netlify deploy --prod --dir=dist
```

#### Option B: Vercel

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Deploy:**
```bash
vercel --prod
```

#### Option C: AWS S3 + CloudFront

1. **Create S3 bucket:**
```bash
aws s3 mb s3://cake-bakery-frontend
```

2. **Upload build:**
```bash
aws s3 sync dist/ s3://cake-bakery-frontend
```

3. **Create CloudFront distribution:**
```bash
# Via AWS Console
```

#### Option D: Manual Nginx

1. **Upload to server:**
```bash
scp -r dist/* ubuntu@server-ip:/var/www/cake-bakery-frontend/
```

2. **Configure Nginx:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    root /var/www/cake-bakery-frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### Step 3: Configure Environment

```bash
# Create frontend .env for production
VITE_API_BASE_URL=https://api.yourdomain.com/api
```

---

## SSL/HTTPS Configuration

### Nginx SSL Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Monitoring & Logging

### Set Up Logging

```bash
# Backend logs with Supervisor
sudo tail -f /var/log/cake-bakery.out.log

# System monitoring
sudo apt-get install htop
htop

# Database monitoring
sudo -u postgres psql -d cake_bakery -c "SELECT * FROM pg_stat_statements;"
```

### Set Up Monitoring Tools

1. **New Relic:**
```bash
pip install newrelic
newrelic-admin generate-config YOUR_KEY newrelic.ini
newrelic-admin run-program gunicorn app:app
```

2. **Sentry (Error tracking):**
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    "https://your-sentry-dsn@sentry.io/project",
    integrations=[FlaskIntegration()]
)
```

---

## Performance Optimization

### Backend Optimization

1. **Enable Caching:**
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/api/recipes/<id>')
@cache.cached(timeout=300)
def get_recipe(id):
    # ...
```

2. **Database Connection Pooling:**
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,
    "pool_recycle": 3600,
    "pool_pre_ping": True,
}
```

3. **Enable Compression:**
```python
from flask_compress import Compress
Compress(app)
```

### Frontend Optimization

1. **Code Splitting:**
```javascript
const Dashboard = lazy(() => import('./pages/DashboardPage'));
```

2. **Image Optimization:**
```bash
npm install image-webpack-loader
```

3. **Minification:**
```bash
npm run build  # Already minifies
```

---

## Backup Strategy

### Database Backup

```bash
# Daily backup
0 2 * * * pg_dump -U bakery_user cake_bakery | gzip > /backups/cake_bakery_$(date +\%Y\%m\%d).sql.gz

# Weekly backup to S3
0 3 * * 0 aws s3 cp /backups/cake_bakery_*.sql.gz s3://cake-bakery-backups/
```

### Restore from Backup

```bash
gunzip cake_bakery_20240101.sql.gz
psql -U bakery_user cake_bakery < cake_bakery_20240101.sql
```

---

## Scaling Strategy

### Horizontal Scaling

1. **Load Balancer (Nginx):**
```nginx
upstream cake_bakery_servers {
    server 192.168.1.10:8000;
    server 192.168.1.11:8000;
    server 192.168.1.12:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://cake_bakery_servers;
    }
}
```

2. **Auto-scaling (AWS):**
- Use AWS EC2 Auto Scaling Groups
- Set up CloudWatch alarms for CPU/Memory
- Configure Elastic Load Balancer

### Caching Layer

```bash
# Install Redis
sudo apt-get install redis-server

# Configure Redis in .env
REDIS_URL=redis://localhost:6379/0
```

---

## Security Checklist

- [ ] Change default passwords
- [ ] Enable firewall (UFW, AWS Security Groups)
- [ ] Set up HTTPS/SSL
- [ ] Enable database backups
- [ ] Configure environment variables securely
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity
- [ ] Enable database encryption
- [ ] Use strong SECRET_KEY
- [ ] Enable CORS only for trusted domains
- [ ] Rate limiting on API endpoints
- [ ] Regular security audits

---

## Rollback Procedure

```bash
# If deployment fails, rollback
git revert HEAD
git push

# Or restore from previous deployment
supervisor restart cake-bakery
```

---

## Continuous Integration/Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          ssh ubuntu@server-ip 'cd /var/www/cake-bakery && git pull && source venv/bin/activate && pip install -r requirements.txt && supervisorctl restart cake-bakery'
      
      - name: Deploy Frontend
        run: |
          npm install
          npm run build
          aws s3 sync dist/ s3://cake-bakery-frontend/
```

---

**Deployment complete! Your Smart Home Bakery Platform is now live! 🚀**
