# 🧪 Pre-Deployment Testing Guide

Complete testing checklist before pushing to production.

---

## Step 1: Local Backend Testing

### 1.1 Setup & Run

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
python app.py
```

### 1.2 Test API Endpoints

Open PowerShell and run these tests:

```powershell
# Test health check
curl http://localhost:5000/api/health

# Test registration
$data = @{
    username = "testuser"
    email = "test@example.com"
    password = "testpass123"
    full_name = "Test User"
} | ConvertTo-Json
curl -Method POST -Uri "http://localhost:5000/api/auth/register" `
    -ContentType "application/json" -Body $data

# Test login
$login = @{
    username = "testuser"
    password = "testpass123"
} | ConvertTo-Json
curl -Method POST -Uri "http://localhost:5000/api/auth/login" `
    -ContentType "application/json" -Body $login
```

### 1.3 Database Test

```powershell
# Check SQLite database created
Test-Path backend/cake_bakery.db
```

---

## Step 2: Local Frontend Testing

### 2.1 Setup & Run

```powershell
cd frontend
npm install
cp .env.example .env
# Verify VITE_API_BASE_URL is http://localhost:5000/api
npm run dev
```

### 2.2 Browser Tests

1. Open http://localhost:3000
2. Test each page:
   - [ ] HomePage loads
   - [ ] Register page (create test account)
   - [ ] Login page (login with test account)
   - [ ] Dashboard loads with data
   - [ ] Recipe Generator works
   - [ ] Inventory page loads
   - [ ] Orders page loads
   - [ ] All sidebar navigation works

### 2.3 API Connection Test

1. Open browser DevTools (F12)
2. Check Network tab while clicking buttons
3. Verify requests go to `http://localhost:5000/api`
4. Check response status codes (200, 201, etc.)

---

## Step 3: Production Build Testing

### 3.1 Frontend Build

```powershell
cd frontend
npm run build
npm run preview
```

1. Visit http://localhost:4173
2. Test all features work in production build
3. Check browser console for errors
4. Verify no `localhost:5000` hardcoded URLs

### 3.2 Backend Production Build

```powershell
cd backend
pip install gunicorn
gunicorn app:app
```

1. Visit http://localhost:8000/api/health
2. Verify it works with production server

---

## Step 4: Database Testing

### 4.1 Schema Verification

```powershell
# Check if all tables exist
sqlite3 backend/cake_bakery.db ".tables"

# Export schema
sqlite3 backend/cake_bakery.db ".schema"
```

### 4.2 Data Integrity Test

```powershell
# Insert test data and verify
sqlite3 backend/cake_bakery.db "
    SELECT COUNT(*) as user_count FROM users;
    SELECT COUNT(*) as recipe_count FROM recipes;
    SELECT COUNT(*) as order_count FROM orders;
"
```

---

## Step 5: AI Integration Testing

### 5.1 Add API Keys

Update `.env` with your keys:

```
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
```

### 5.2 Test Recipe Generation

1. Login to frontend
2. Go to Recipe Generator
3. Fill form and click "Generate Recipe"
4. Check backend logs for API call
5. Verify recipe displays

### 5.3 Test Other AI Features

- [ ] Decoration recommendations work
- [ ] Problem diagnosis works
- [ ] Profit optimization works

---

## Step 6: Full Flow Testing

Complete user journey:

1. **Register** - Create new account
2. **Add Ingredients** - Add 3+ ingredients to inventory
3. **Generate Recipe** - Use AI to generate a cake recipe
4. **Create Order** - Create a new order
5. **Estimate Cost** - Estimate the order cost
6. **Finalize Order** - Complete the order
7. **Check Dashboard** - Verify profit is calculated
8. **Logout** - End session
9. **Login** - Verify session persistence
10. **Check Data** - All data still there after login

---

## Step 7: Error Handling Testing

Test how app handles errors:

1. **Network Error:** Unplug internet, try API call → Should show error toast
2. **Invalid Input:** Register with invalid email → Should show validation error
3. **Duplicate Data:** Try to register same email twice → Should show error
4. **Missing Fields:** Submit form without required fields → Should not submit
5. **Server Error:** Stop backend, try API call → Should show connection error

---

## Step 8: Performance Testing

### 8.1 Build Size

```powershell
cd frontend
npm run build
# Check dist/ folder size (should be < 500KB gzipped)
```

### 8.2 Load Time

1. Open DevTools (F12)
2. Go to Performance tab
3. Record page load
4. Check metrics:
   - First Contentful Paint: < 1.5s
   - Largest Contentful Paint: < 2.5s
   - Total Blocking Time: < 100ms

### 8.3 API Response Time

1. Check Network tab in DevTools
2. Each API call should be < 500ms
3. Database queries should be < 200ms

---

## Step 9: Security Testing

### 9.1 Authentication

- [ ] Cannot access protected routes without login
- [ ] Token expires after logout
- [ ] Cannot modify other user's data
- [ ] Password is not logged anywhere

### 9.2 Input Validation

- [ ] XSS attacks are prevented
- [ ] SQL injection is prevented (SQLAlchemy prevents this)
- [ ] Large file uploads are rejected

### 9.3 API Security

- [ ] Rate limiting works (if implemented)
- [ ] Sensitive data is not logged
- [ ] Error messages don't leak information

---

## Step 10: Browser Compatibility

Test on:

- [ ] Chrome (Latest)
- [ ] Firefox (Latest)
- [ ] Safari (Latest)
- [ ] Edge (Latest)
- [ ] Mobile Chrome
- [ ] Mobile Safari

---

## Pre-Deployment Checklist

Before pushing to production:

```
✅ All tests pass
✅ No console errors
✅ No network errors in DevTools
✅ Database has test data
✅ API calls work end-to-end
✅ Production build runs without errors
✅ Environment variables are correct
✅ Security checks pass
✅ Performance is acceptable
✅ All browser compatibility tests pass
✅ User can complete full flow
✅ Error handling works correctly
```

---

## Troubleshooting

### Backend won't start

```powershell
# Check port is free
netstat -ano | findstr :5000

# Kill process using port 5000
Stop-Process -Id <PID> -Force

# Check Python version
python --version  # Should be 3.8+
```

### Frontend won't build

```powershell
# Clear node_modules
rm -r frontend/node_modules
npm install

# Check Node version
node --version  # Should be 14+
```

### API not connecting

- Check `VITE_API_BASE_URL` in frontend .env
- Check backend is running
- Check CORS settings
- Check firewall isn't blocking port 5000

---

**Ready to Deploy?** ✅ 

Once all steps pass, commit and push to GitHub, then proceed with cloud deployment!
