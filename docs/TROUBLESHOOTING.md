# Troubleshooting Guide

## Common Issues and Solutions

### Backend Issues

#### 1. Flask Application Won't Start

**Problem:** `Error: The Flask application is not loading`

**Solutions:**
```bash
# Clear Python cache
rm -r backend/__pycache__
rm backend/*.pyc

# Verify virtual environment is activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check for syntax errors
python -m py_compile app.py
```

#### 2. Database Connection Error

**Problem:** `sqlite3.OperationalError: database is locked` or database doesn't exist

**Solutions:**
```bash
# Remove old database and reinitialize
rm backend/cake_bakery.db

# Start Flask app to create new database
python app.py

# If using different database:
# Check DATABASE_URL in .env
```

**For PostgreSQL connection issues:**
```bash
# Test connection
psql -h localhost -U username -d cake_bakery

# Ensure PostgreSQL is running:
# macOS:
brew services start postgresql

# Ubuntu:
sudo systemctl start postgresql

# Windows: Start PostgreSQL service
```

#### 3. API Returns 500 Error

**Problem:** Internal server error on API calls

**Solutions:**
```bash
# Check server logs
# Look at terminal where Flask is running for error messages

# Enable debug mode in .env
FLASK_ENV=development
FLASK_DEBUG=1

# Check for missing environment variables
# Ensure .env has all required keys

# Validate request data
# Make sure POST data is valid JSON
```

#### 4. CORS Error: No 'Access-Control-Allow-Origin' Header

**Problem:** Frontend can't connect to backend due to CORS

**Solutions:**
1. Check `.env` in backend:
   ```
   CORS_ORIGINS=http://localhost:3000
   ```

2. Restart backend server after changing .env

3. Clear browser cache and restart

4. Check frontend API URL in `.env`:
   ```
   VITE_API_BASE_URL=http://localhost:5000/api
   ```

#### 5. OpenAI API Key Error

**Problem:** `Error: Invalid API key` or `401 Unauthorized`

**Solutions:**
```bash
# Verify API key is correct
# Go to https://platform.openai.com/api-keys
# Copy full key (including sk- prefix)

# Update .env
OPENAI_API_KEY=sk-your-actual-key-here

# Restart Flask app

# Check for trailing/leading spaces
# Keys are case-sensitive
```

**Test OpenAI connection:**
```python
import openai
openai.api_key = "your-api-key"
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response)
```

#### 6. Port Already in Use

**Problem:** `Address already in use` error

**Solutions:**
```bash
# Windows - Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux - Find and kill process on port 5000
lsof -i :5000
kill -9 <PID>

# Or change port in config.py
SERVER_PORT = 5001
```

#### 7. Module Import Error

**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solutions:**
```bash
# Activate virtual environment first
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Verify installation
pip list | grep flask

# Reinstall if needed
pip install flask==2.3.3
```

#### 8. SQLAlchemy Model Errors

**Problem:** `No column named 'X'` or relationship errors

**Solutions:**
```bash
# Regenerate database
rm cake_bakery.db
python app.py

# Check model definitions in models/database.py
# Verify column names match between models and database

# For migrations (if using Alembic)
flask db upgrade
```

---

### Frontend Issues

#### 1. npm Install Fails

**Problem:** `npm ERR! code ERESOLVE` or dependency conflicts

**Solutions:**
```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and lock file
rm -r node_modules package-lock.json
npm install

# Use legacy peer deps if needed
npm install --legacy-peer-deps
```

#### 2. Port 3000 Already in Use

**Problem:** `Port 3000 is already in use`

**Solutions:**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :3000
kill -9 <PID>

# Vite will auto-use next available port
```

#### 3. Cannot Reach Backend API

**Problem:** `Failed to connect to http://localhost:5000` or CORS errors

**Solutions:**
1. Verify backend is running: http://localhost:5000/api/health
2. Check `VITE_API_BASE_URL` in frontend `.env`
3. Restart frontend dev server
4. Check browser console for exact error

#### 4. Components Not Loading

**Problem:** Page appears blank or components not rendering

**Solutions:**
```bash
# Check browser console for errors (F12)
# Look for React errors

# Clear browser cache
# Hard refresh: Ctrl+Shift+R (Cmd+Shift+R on Mac)

# Rebuild project
rm -r node_modules dist
npm install
npm run dev

# Check for console errors
# Fix TypeScript errors if any
```

#### 5. State Not Updating

**Problem:** Zustand store state not updating in components

**Solutions:**
1. Verify store exports are correct in `services/store.js`
2. Check component imports are correct
3. Ensure state updates use proper syntax
4. Use React DevTools to inspect Zustand store

#### 6. Dark Mode Not Working

**Problem:** Dark mode toggle doesn't change theme

**Solutions:**
```javascript
// Check localStorage is available
console.log(localStorage.getItem('darkMode'))

// Verify CSS classes are applied
// Check browser inspector for theme classes

// Reset theme preference
localStorage.removeItem('darkMode')
localStorage.setItem('darkMode', 'false')
```

#### 7. Form Submission Not Working

**Problem:** Form doesn't submit or submit button doesn't respond

**Solutions:**
1. Check form validation rules
2. Verify API endpoint in api.js matches backend
3. Check for JavaScript errors in console
4. Verify network tab in DevTools for API request
5. Check backend is receiving request

#### 8. Images Not Loading

**Problem:** Cake images from DALL-E not displaying

**Solutions:**
```bash
# Check if image URL is valid
# Verify CORS allows image loading from external source
# Check image URL in Network tab

# Test with direct URL in browser
# Check image expiration (DALL-E images expire)
```

---

### Database Issues

#### 1. Database File Corruption

**Problem:** `database disk image is malformed` or database read errors

**Solutions:**
```bash
# Backup current database
cp cake_bakery.db cake_bakery.db.backup

# Delete corrupted database
rm cake_bakery.db

# Reinitialize
python app.py

# Restore data from backup if needed
sqlite3 cake_bakery.db < backup.sql
```

#### 2. Foreign Key Constraint Violation

**Problem:** `FOREIGN KEY constraint failed`

**Solutions:**
```bash
# Ensure parent record exists before creating child
# Check relationship definitions in models/database.py

# Enable foreign key constraints
# In backend config: SQLALCHEMY_DATABASE_URI with ?check_same_thread=false
```

#### 3. Database Query Timeout

**Problem:** Long-running queries freeze application

**Solutions:**
```bash
# Add query indexes for frequently searched fields
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_recipes_cake_type ON recipes(cake_type);

# Implement pagination (already done in backend)
# Avoid N+1 query problems with lazy='select' or 'joined'
```

---

### AI Service Issues

#### 1. Recipe Generation Fails

**Problem:** AI-generated recipes return empty or errors

**Solutions:**
1. Verify API keys are valid and have credits
2. Check parameters are within valid ranges:
   - Cake weight: 500g, 1kg, 2kg, 3kg
   - Servings: 1-24
   - Budget: positive number

3. Test with simpler parameters first

4. Check network connectivity

5. Verify response parsing in `ai_service.py`

#### 2. Fallback to Gemini Not Working

**Problem:** OpenAI fails but Gemini doesn't kick in

**Solutions:**
```bash
# Verify both API keys are set in .env
OPENAI_API_KEY=...
GEMINI_API_KEY=...

# Check fallback logic in ai_service.py
# Ensure try-except blocks are correct

# Test Gemini API directly
python
>>> from services.ai_service import AIService
>>> service = AIService()
>>> service.generate_recipe(..., ai_provider='gemini')
```

#### 3. Image Generation Not Working

**Problem:** DALL-E image generation returns error or no image

**Solutions:**
1. Verify OpenAI API key has image generation permission
2. Check image prompt is under 1000 characters
3. Verify API quota hasn't exceeded
4. Check response parsing in code

---

### Performance Issues

#### 1. Backend Slow Response

**Problem:** API requests take too long to respond

**Solutions:**
```bash
# Check database indexes exist
# See DATABASE.md for index creation

# Monitor slow queries in Flask logs
# Enable query logging

# Implement caching (Redis recommended)
# Use pagination to limit results

# Profile with Python profiler
python -m cProfile -s cumulative app.py
```

#### 2. Frontend Slow Loading

**Problem:** Page takes long time to load

**Solutions:**
```bash
# Analyze bundle size
npm run build
npm run analyze

# Use React DevTools Profiler
# Check Network tab for slow requests

# Implement code splitting
# Use lazy loading for routes

# Optimize images
# Minimize CSS/JavaScript
```

#### 3. Database Slow Queries

**Problem:** Specific operations are very slow

**Solutions:**
```bash
# Check database indexes
sqlite3 cake_bakery.db ".indices"

# Analyze query plan
EXPLAIN QUERY PLAN SELECT * FROM recipes WHERE cake_type='Chocolate';

# Add missing indexes
# Archive old data periodically
# Use pagination
```

---

### Deployment Issues

#### 1. Application Works Locally But Not on Server

**Problem:** Production deployment fails

**Solutions:**
1. Check environment variables are set correctly
2. Verify database is initialized on server
3. Check logs on server
4. Test with `gunicorn` locally
5. Verify all dependencies installed

#### 2. HTTPS Certificate Issues

**Problem:** SSL certificate errors

**Solutions:**
```bash
# Use Let's Encrypt for free certificates
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d yourdomain.com

# Configure Flask to use HTTPS
```

#### 3. Memory Issues on Server

**Problem:** Application runs out of memory

**Solutions:**
1. Monitor with: `top` or `htop`
2. Reduce worker count in gunicorn
3. Implement caching
4. Archive old database records
5. Use database connection pooling

---

## Debugging Tips

### 1. Enable Debug Logging

**Backend:**
```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
```javascript
// In components
console.log('Debug info:', variableName);
```

### 2. Use Browser DevTools

1. **Elements Tab**: Inspect HTML elements
2. **Console Tab**: See JavaScript errors and logs
3. **Network Tab**: Monitor API requests and responses
4. **Application Tab**: Check localStorage and cookies
5. **Performance Tab**: Profile page load time

### 3. Use VS Code Debugger

**Backend:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "development",
        "FLASK_DEBUG": "1"
      },
      "args": ["run"],
      "jinja": true
    }
  ]
}
```

### 4. Database Inspection

```bash
# SQLite CLI
sqlite3 cake_bakery.db

# Show schema
.schema

# Show tables
.tables

# Run SQL query
SELECT * FROM users;

# Export data
.output data.csv
SELECT * FROM recipes;
.output stdout
```

---

## Getting Help

1. **Check logs** - Most useful information is in logs
2. **Search documentation** - See docs/ folder
3. **Recreate issue** - Minimal reproduction example
4. **Check similar issues** - GitHub issues section
5. **Review code** - Check related source files

---

**Still having issues? Create a GitHub issue with:**
- Error message (full text)
- Steps to reproduce
- Environment details
- Relevant code/logs
- Screenshot if visual issue

---

**Happy debugging! 🔧**
