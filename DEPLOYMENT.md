# 🚀 Production Deployment Guide

Complete step-by-step guide to deploy Smart Home Bakery Platform to production.

---

## Part 1: GitHub Setup (Fix Push Issue)

### Step 1: Authenticate with GitHub

**Option A: Using Personal Access Token (Recommended for Windows)**

1. Go to https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Give it a name: `CAKE-Platform-Deploy`
4. Select scopes: `repo` (full access)
5. Click **Generate token** and **copy it**
6. In PowerShell, run:
   ```powershell
   git push -u origin main
   ```
7. When prompted for password, paste your **Personal Access Token** (not your GitHub password)

**Option B: Using SSH (More Secure)**

1. Generate SSH key:
   ```powershell
   ssh-keygen -t ed25519 -C "your-email@example.com"
   ```
2. Press Enter three times (default location, no passphrase)
3. Add SSH key to GitHub:
   - Go to https://github.com/settings/ssh
   - Click **New SSH key**
   - Paste output from: `cat $env:USERPROFILE\.ssh\id_ed25519.pub`
4. Change remote to SSH:
   ```powershell
   git remote set-url origin git@github.com:mihir2452005/Smart-Home-Bakery-Management-Platform.git
   ```
5. Push to GitHub:
   ```powershell
   git push -u origin main
   ```

### Step 2: Verify Push

```powershell
git push origin main
```

---

## Part 2: Database Setup (Supabase - Free)

### Step 1: Create Supabase Project

1. Go to https://supabase.com
2. Click **Start your project**
3. Sign up with GitHub (easiest)
4. Create a new project:
   - **Project Name:** `smart-bakery`
   - **Database Password:** Save this securely
   - **Region:** Choose closest to your users
5. Wait for database creation (2-3 minutes)

### Step 2: Get Connection String

1. In Supabase dashboard, click **Settings** → **Database**
2. Copy the **Connection String** (URI) under "Connection pooling"
3. It looks like: `postgresql://postgres:PASSWORD@host:5432/postgres`
4. **Save this securely** - you'll need it for backend deployment

### Step 3: Initialize Database Schema

1. Download and install **DBeaver** (free database tool) or use **pgAdmin**
2. Create new connection:
   - **Host:** Your Supabase host (from connection string)
   - **Database:** postgres
   - **User:** postgres
   - **Password:** Your Supabase password
3. Open the database connection
4. Run the SQL from `backend/database/schema.sql`:
   - Copy entire schema.sql content
   - Paste into DBeaver's SQL editor
   - Execute

---

## Part 3: Backend Deployment (Render.com - Free)

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Authorize access to your repositories

### Step 2: Create Web Service

1. In Render dashboard, click **New +** → **Web Service**
2. Select your GitHub repository: `Smart-Home-Bakery-Management-Platform`
3. Configure:
   - **Name:** `smart-bakery-api`
   - **Environment:** `Python 3`
   - **Region:** Choose closest to users
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free (or Starter if you need better performance)

### Step 3: Add Environment Variables

In Render dashboard, under your service:
1. Click **Environment**
2. Add each variable:

```
FLASK_ENV=production
SECRET_KEY=<Generate: python -c "import secrets; print(secrets.token_hex(32))">
DATABASE_URL=<Your Supabase connection string>
OPENAI_API_KEY=<Your OpenAI API key from https://platform.openai.com/api-keys>
GEMINI_API_KEY=<Your Gemini API key from https://makersuite.google.com/app/apikey>
CORS_ORIGINS=https://<your-vercel-url>.vercel.app,http://localhost:3000
SERVER_PORT=5000
```

**Important:** Do NOT include `http://` or `https://` in CORS_ORIGINS values. Use comma-separated list for multiple origins.

### Step 4: Get Backend URL

1. After deployment completes, you'll see a URL like:
   ```
   https://smart-bakery-api.onrender.com
   ```
2. **Save this** - you need it for frontend

### Step 5: Test Backend

Visit: `https://smart-bakery-api.onrender.com/api/health`

You should see:
```json
{
  "status": "success",
  "message": "Smart Home Bakery API is running!"
}
```

---

## Part 4: Frontend Deployment (Vercel)

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub
3. Authorize access

### Step 2: Import Project

1. Click **Add New** → **Project**
2. Find and select: `Smart-Home-Bakery-Management-Platform`
3. Configure:
   - **Framework:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`

### Step 3: Add Environment Variables

In Vercel project settings:
1. Click **Settings** → **Environment Variables**
2. Add:

```
VITE_API_BASE_URL=https://smart-bakery-api.onrender.com/api
```

### Step 4: Deploy

1. Click **Deploy**
2. Vercel will build and deploy your frontend
3. You'll get a URL like: `https://smart-bakery.vercel.app`

### Step 5: Update Backend CORS

Go back to Render dashboard:
1. Update `CORS_ORIGINS` to include your Vercel URL:
   ```
   https://smart-bakery.vercel.app,http://localhost:3000
   ```
2. Redeploy backend by clicking **Manual Deploy** → **Deploy latest commit**

---

## Part 5: Verification Checklist

- [ ] GitHub repo has all code pushed
- [ ] Supabase database is created and schema loaded
- [ ] Backend deployed on Render and `/api/health` returns 200
- [ ] Frontend deployed on Vercel
- [ ] CORS is configured correctly
- [ ] API calls from frontend to backend work
- [ ] AI API keys are set and working
- [ ] Database queries work (test by registering a new user)

---

## Part 6: Post-Deployment Tasks

### 1. Test Full Flow

1. Go to your Vercel URL
2. Register a new account
3. Generate a recipe
4. Create an order
5. Check dashboard

### 2. Set Up AI API Keys

**OpenAI:**
- Go to https://platform.openai.com/api-keys
- Create new API key
- Add to Render environment variables
- Minimum account balance required (~$5)

**Google Gemini:**
- Go to https://makersuite.google.com/app/apikey
- Create new API key
- Add to Render environment variables
- Free tier available

### 3. Monitor Performance

- **Render:** Check logs at https://render.com/dashboard
- **Vercel:** Check logs at https://vercel.com/dashboard
- **Supabase:** Monitor usage at https://supabase.com/dashboard

### 4. Set Up Backups

In Supabase:
1. Click **Settings** → **Database**
2. Enable **Automatic backups**
3. Set retention to 7 days (free tier)

---

## Part 7: Common Issues & Solutions

### Issue: "Connection refused" from frontend to backend

**Solution:**
- Check `VITE_API_BASE_URL` in Vercel environment
- Ensure Render backend is running (check logs)
- Verify CORS_ORIGINS includes Vercel URL
- Wait 30 seconds for Render to redeploy after updating CORS

### Issue: Database queries failing

**Solution:**
- Verify `DATABASE_URL` is correct (test in DBeaver first)
- Ensure schema.sql was fully executed
- Check database user has proper permissions

### Issue: AI endpoints returning 400

**Solution:**
- Verify API keys are correct
- Check you have sufficient API balance/quota
- Test API key manually at provider's dashboard

### Issue: Vercel build failing

**Solution:**
- Check build logs: `npm run build` locally
- Verify `vite.config.js` is correct
- Clear cache: Go to Vercel Settings → Deployments → Clear Cache

---

## Part 8: Performance Optimization (Production)

### Backend
1. Enable gzip compression
2. Set up Redis caching (optional)
3. Optimize database queries with indexes
4. Use connection pooling (Supabase provides this)

### Frontend
1. Enable minification (Vite does this by default)
2. Set up CDN caching
3. Use image optimization

### Database
1. Set up read replicas for large queries
2. Archive old orders/recipes
3. Index frequently queried columns

---

## Part 9: Scaling to Multiple Users

When you have many users:

1. **Upgrade Render:** Change from Free to Starter tier (~$7/month)
2. **Upgrade Supabase:** Upgrade database tier for better performance
3. **Add Redis:** For caching frequently used data
4. **Set up email service:** SendGrid or Mailgun for notifications
5. **Enable rate limiting:** Protect API from abuse

---

## Part 10: Domain Configuration (Optional)

### Add Custom Domain to Vercel

1. Go to Vercel project → **Settings** → **Domains**
2. Add your domain (e.g., `smartbakery.com`)
3. Follow DNS configuration instructions
4. Update `CORS_ORIGINS` on Render to include your domain

---

## 🎉 Congratulations!

Your Smart Home Bakery Platform is now live in production! 🍰

**Next Steps:**
- Share the URL with beta testers
- Gather feedback
- Iterate on features
- Monitor performance and costs

