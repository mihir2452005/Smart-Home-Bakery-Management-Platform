# Setup Guide

## Prerequisites

### System Requirements
- **Python:** 3.8+
- **Node.js:** 16+ and npm 7+
- **Database:** SQLite (included with Python) or PostgreSQL for production
- **Git:** For version control

### Required API Keys
- **OpenAI API Key:** For recipe and image generation
- **Google Gemini API Key:** As backup AI provider (optional)

## Backend Setup (Flask)

### Step 1: Clone and Navigate

```bash
cd backend
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
# Important variables:
# - OPENAI_API_KEY: Your OpenAI API key
# - GEMINI_API_KEY: Your Google Gemini API key
# - SECRET_KEY: Change to a secure random string
# - DATABASE_URL: sqlite:///cake_bakery.db (for development)
```

### Step 5: Initialize Database

```bash
# Using Flask CLI
python app.py

# Or manually initialize
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

### Step 6: Run Development Server

```bash
python app.py
```

Server will start on `http://localhost:5000`

### Step 7: Verify Backend

Test the health endpoint:
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "success",
  "message": "Smart Home Bakery API is running!"
}
```

## Frontend Setup (React)

### Step 1: Navigate to Frontend

```bash
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

This will install:
- React 18
- Tailwind CSS
- Axios
- Zustand
- React Router
- And other dependencies

### Step 3: Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env (typically no changes needed for local development)
# VITE_API_BASE_URL=http://localhost:5000/api
```

### Step 4: Start Development Server

```bash
npm run dev
```

Frontend will start on `http://localhost:3000`

### Step 5: Build for Production

```bash
npm run build
```

Output will be in the `dist/` folder

## API Keys Setup

### OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy and add to `.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

### Google Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy and add to `.env`:
   ```
   GEMINI_API_KEY=your-gemini-key-here
   ```

## Project Structure Verification

After setup, your structure should look like:

```
CAKE/
├── backend/
│   ├── venv/              ← Virtual environment (created)
│   ├── app.py
│   ├── config.py
│   ├── cake_bakery.db     ← Database (created)
│   ├── .env               ← Configuration (created from .env.example)
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── ...
├── frontend/
│   ├── node_modules/      ← Dependencies (created)
│   ├── src/
│   ├── public/
│   ├── .env               ← Configuration (created from .env.example)
│   └── package.json
└── docs/
```

## Common Setup Issues

### Issue: `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Then install dependencies
pip install -r requirements.txt
```

### Issue: `npm: command not found`

**Solution:**
- Install Node.js from https://nodejs.org/
- Verify installation: `node --version` and `npm --version`

### Issue: Port 5000 or 3000 already in use

**Backend (change port in config.py):**
```python
SERVER_PORT = 5001  # Change to available port
```

**Frontend (Vite automatically uses next available port)**

### Issue: Database locked error

**Solution:**
```bash
# Remove the old database
rm cake_bakery.db

# Reinitialize
python app.py
```

### Issue: CORS errors in frontend

**Solution:**
Verify `CORS_ORIGINS` in `.env`:
```
CORS_ORIGINS=http://localhost:3000
```

## Testing the Full Stack

### 1. Start Backend

```bash
cd backend
python app.py
```

Wait for: "Running on http://127.0.0.1:5000"

### 2. Start Frontend (in new terminal)

```bash
cd frontend
npm run dev
```

Wait for: "VITE v... ready in ... ms"

### 3. Test Registration

1. Open http://localhost:3000
2. Click "Register"
3. Fill in details:
   - Username: `test_baker`
   - Email: `test@example.com`
   - Password: `password123`
   - Full Name: `Test Baker`

### 4. Test Login

1. Use the credentials from registration
2. You should see the dashboard

### 5. Test Recipe Generation

1. Go to "Recipe Generator"
2. Fill in:
   - Cake Flavor: Chocolate
   - Weight: 1kg
   - Budget: ₹500
   - Oven Type: Gas Oven
3. Click "Generate Recipe"

## Database Setup for Production

### Using PostgreSQL

1. **Install PostgreSQL**
   ```bash
   # macOS
   brew install postgresql

   # Ubuntu
   sudo apt-get install postgresql

   # Windows
   # Download from https://www.postgresql.org/download/windows/
   ```

2. **Create Database**
   ```bash
   createdb cake_bakery
   ```

3. **Update .env**
   ```
   DATABASE_URL=postgresql://username:password@localhost/cake_bakery
   ```

4. **Install PostgreSQL adapter**
   ```bash
   pip install psycopg2-binary
   ```

## Deployment Checklist

### Backend

- [ ] Update `SECRET_KEY` in `.env` to a secure random string
- [ ] Set `FLASK_ENV=production`
- [ ] Enable `SESSION_COOKIE_SECURE=True`
- [ ] Set up proper logging
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure gunicorn worker count
- [ ] Set up proper environment variables
- [ ] Test error handling
- [ ] Set up rate limiting
- [ ] Enable HTTPS
- [ ] Set up monitoring/alerts

### Frontend

- [ ] Build the production bundle: `npm run build`
- [ ] Test production build locally: `npm run preview`
- [ ] Optimize images
- [ ] Minify CSS/JS
- [ ] Set up analytics
- [ ] Configure CDN
- [ ] Set up monitoring

## Useful Commands

### Backend

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install new package
pip install package_name

# Generate requirements.txt
pip freeze > requirements.txt

# Run tests
pytest

# Format code
black .

# Lint code
flake8

# Database migration (if using Alembic)
flask db upgrade
```

### Frontend

```bash
# Install new package
npm install package_name

# Remove package
npm uninstall package_name

# Lint code
npm run lint

# Format code
npm run format

# Analyze bundle size
npm run analyze

# Generate production build
npm run build
```

## Performance Tips

### Backend
- Enable query optimization
- Set up Redis for caching
- Use connection pooling for database
- Implement request compression
- Set up CDN for static files

### Frontend
- Code splitting
- Lazy loading
- Image optimization
- Browser caching
- Minification

## Security Checklist

- [ ] Validate all user inputs
- [ ] Sanitize database queries (using ORM)
- [ ] Implement CSRF protection
- [ ] Use HTTPS
- [ ] Hash passwords properly
- [ ] Rate limit API endpoints
- [ ] Implement proper authentication
- [ ] Use environment variables for secrets
- [ ] Enable CORS properly
- [ ] Set security headers
- [ ] Regular security audits
- [ ] Keep dependencies updated

## Support & Troubleshooting

### Documentation
- API Documentation: `docs/API.md`
- Database Schema: `docs/DATABASE.md`
- Features: `docs/FEATURES.md`

### Getting Help

1. **Check existing issues** on GitHub
2. **Search documentation**
3. **Create new issue** with:
   - Error message
   - Steps to reproduce
   - Environment details
   - Screenshots

### Useful Links

- Flask Documentation: https://flask.palletsprojects.com/
- React Documentation: https://react.dev/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Tailwind CSS: https://tailwindcss.com/docs
- OpenAI API: https://platform.openai.com/docs/
- Google Gemini: https://ai.google.dev/docs

---

**You're all set! Happy developing! 🎂**
