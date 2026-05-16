# Razorpay Payment Configuration Guide

## Website Information

**Website URL**: `https://smart-home-bakery-platform.vercel.app`

**Payment Gateway**: Razorpay (India's Leading Payment Gateway)

**Login Requirement**: **NO** (Users can pay as guests or logged-in users)

---

## 🎯 Payment Configuration

### Website Profile
- **Website**: https://smart-home-bakery-platform.vercel.app
- **Business Type**: SaaS (Software as a Service)
- **Service**: AI-Powered Bakery Management Platform
- **Payment Acceptance**: Both Logged-In & Guest Users
- **Test Account**: Optional (see below)

---

## 📋 Razorpay Setup Checklist

### Step 1: Create Razorpay Merchant Account
1. Go to https://razorpay.com
2. Click **"Sign Up"** → Choose **"Business"**
3. Fill in business details:
   - Business Name: **Cake Hub** (or your company name)
   - Website: **https://smart-home-bakery-platform.vercel.app**
   - Business Type: **SaaS / Software**
4. Complete KYC verification (10-15 minutes)
5. Get **API Keys** from Dashboard → Settings → API Keys

### Step 2: Configure API Keys

**Live Keys** (Production - Real Money):
```
Key ID:     rzp_live_xxxxxxxxxxxxx
Key Secret: your_live_secret_key
```

**Test Keys** (Development - Fake Money):
```
Key ID:     rzp_test_1DP5mmOlF5G5ag (Already configured)
Key Secret: test_secret_key (Already configured)
```

### Step 3: Update Environment Variables

**Backend** (`.env` or Render environment variables):
```env
# Razorpay Configuration
RAZORPAY_KEY_ID=rzp_test_1DP5mmOlF5G5ag
RAZORPAY_KEY_SECRET=test_secret_key

# Database
DATABASE_URL=postgresql://...
```

**Frontend** (`.env` or Vercel environment variables):
```env
# Razorpay Configuration
REACT_APP_RAZORPAY_KEY=rzp_test_1DP5mmOlF5G5ag
REACT_APP_API_URL=https://cake-backend.onrender.com

# Optional
REACT_APP_BUSINESS_NAME=Cake Hub
```

---

## 🧪 Test Account Credentials

### Test Payment Methods

**For UPI:**
- **Virtual ID**: `success@razorpay`
- **Status**: Payment succeeds

**For Cards (Visa/Mastercard):**
- **Test Card**: `4111 1111 1111 1111`
- **Expiry**: Any future date (e.g., `12/25`)
- **CVV**: Any 3 digits (e.g., `123`)
- **Status**: Payment succeeds

**For Netbanking:**
- Use any bank in the dropdown
- **Status**: Payment succeeds

**For Digital Wallets:**
- Select any wallet (Paytm, PhonePe, etc.)
- **Status**: Payment succeeds

---

## 💳 Payment Methods Enabled

### Supported Payment Methods
```
✅ UPI (Google Pay, PhonePe, Paytm, WhatsApp Pay)
✅ Credit Cards (Visa, Mastercard, Amex)
✅ Debit Cards (All banks)
✅ Net Banking (50+ Indian banks)
✅ Digital Wallets (Paytm, Mobikwik, FreeCharge)
✅ EMI (Credit cards + Bajaj Finance)
```

**Currently Enabled:**
```javascript
method: {
  upi: true,        // ✅ 
  card: true,       // ✅ 
  netbanking: true, // ✅ 
  wallet: true,     // ✅ 
}
```

---

## 🔐 Payment Flow (With/Without Login)

### Option A: Guest User Checkout (Recommended)
```
1. User on homepage
2. Click "Start Free Trial" (₹299/month plan)
3. Enter name, email, phone
4. Razorpay payment form opens
5. Pay via UPI/Card/Netbanking/Wallet
6. Account created automatically after payment
7. Subscription activated
8. Access platform
```

### Option B: Logged-In User
```
1. User logs in to platform
2. Go to pricing page
3. Click "Upgrade to Professional"
4. Payment processed with logged-in user info
5. Subscription updated
6. Premium features unlocked
```

**Current Implementation**: Supports BOTH flows automatically

---

## 📊 Payment Pricing

### Plan Configuration

| Plan | Price | Payment | Duration | Features |
|------|-------|---------|----------|----------|
| **Hobby** | Free | None | 30 days | 10 recipes, basic analytics |
| **Professional** | ₹299 | UPI/Card | 30 days | Unlimited recipes, full analytics |
| **Enterprise** | Custom | Invoice | 1 year | Everything + support |

### Change Pricing

**File**: `backend/routes/payments.py` (Lines 33)

```python
'professional': {
    'amount': 29900,  # ₹299 in paise (100 paise = ₹1)
    # To change to ₹499: use 49900
    # To change to ₹199: use 19900
    'duration_days': 30,  # Monthly billing
}
```

---

## 🌐 Website Integration

### How It Works

1. **Pricing Page** (`frontend/src/pages/HomePage.jsx`):
   - Shows 3 pricing tiers
   - Buttons linked to payment flow

2. **Payment Service** (`frontend/src/services/paymentService.js`):
   - Loads Razorpay SDK
   - Creates payment orders
   - Verifies signatures
   - Supports guest & logged-in users

3. **Backend API** (`backend/routes/payments.py`):
   - `POST /api/payments/create-order` - Creates Razorpay order
   - `POST /api/payments/verify` - Verifies payment
   - `POST /api/payments/free-signup` - Creates free accounts
   - `GET /api/payments/subscription/{user_id}` - Gets subscription status

4. **Database** (`Subscription` table):
   - Stores plan, status, expiry, payment ID
   - Tracks all transactions

---

## 🚀 Going Live

### Before Going Live
- [ ] Switch from test keys to live keys
- [ ] Test with real payment (small amount)
- [ ] Verify email notifications work
- [ ] Set up backup & monitoring
- [ ] Enable webhooks for notifications

### Deployment Steps

1. **Get Live Keys**:
   - Dashboard → Settings → API Keys → Live
   - Copy Key ID and Key Secret

2. **Update Backend** (Render):
   ```
   Dashboard → Environment Variables
   RAZORPAY_KEY_ID = rzp_live_xxxxxxxxxxxxx
   RAZORPAY_KEY_SECRET = your_live_secret
   ```

3. **Update Frontend** (Vercel):
   ```
   Project Settings → Environment Variables
   REACT_APP_RAZORPAY_KEY = rzp_live_xxxxxxxxxxxxx
   ```

4. **Redeploy**:
   - Push changes to GitHub
   - Vercel auto-deploys frontend
   - Render auto-deploys backend

---

## 📞 Customer Payment Details

### Per Transaction, Razorpay Captures:
- Customer Name
- Customer Email
- Customer Phone
- Payment Method
- Transaction Amount
- Payment ID (for tracking)
- Timestamp

### Your Database Captures:
- User ID
- Plan Name
- Subscription Status
- Expiry Date
- Payment ID (linked to Razorpay)

---

## 💰 Pricing Model

### Transaction Fees
- **Razorpay Charges**: 2-3% per transaction (standard India rate)
- **Example**: ₹299 payment → ~₹9-₹9 fee charged
- **You Receive**: ~₹290 per subscription

### Revenue Calculation
```
Plan Price:           ₹299
Razorpay Fee (3%):    -₹8.97
Net Revenue:          ₹290.03
```

---

## 🔔 Webhooks & Notifications

### Optional: Email Notifications After Payment

To add payment confirmation emails:

**File**: `backend/routes/payments.py` (After line 125)

```python
# Send confirmation email
send_email(
    to_email=user.email,
    subject='Payment Received - Welcome to Cake Hub!',
    template='payment_confirmation',
    data={
        'name': user.full_name,
        'plan': plan,
        'expiry_date': expiry_date,
        'payment_id': razorpay_payment_id
    }
)
```

---

## 🛡️ Security Features

✅ **Signature Verification**: Every payment verified with Razorpay signature
✅ **HTTPS Only**: All connections encrypted
✅ **No Card Storage**: Razorpay handles all PCI compliance
✅ **Test Mode**: Full test environment available
✅ **Environment Variables**: Keys never committed to Git

---

## 📈 Monitor Payments

### Razorpay Dashboard
- Go to https://dashboard.razorpay.com
- View all transactions in real-time
- Download reports
- Manage refunds
- View customer details

### Your Backend
- Check `subscriptions` table
- View `razorpay_payment_id` for transaction tracking
- Monitor subscription expiry dates

---

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| "Payment gateway error" | Check API keys in env variables |
| "Invalid signature" | Verify key secret matches Razorpay |
| "Amount too small" | Razorpay has minimum ₹1 limit |
| "Country not supported" | Free plan available (₹0) |
| "Test payment not working" | Use test credentials, test UPI: `success@razorpay` |

---

## 📚 Documentation Links

- **Razorpay Docs**: https://razorpay.com/docs/
- **Razorpay Dashboard**: https://dashboard.razorpay.com
- **Payment Status**: https://razorpay.com/docs/payments/payments-api/
- **Webhooks**: https://razorpay.com/docs/webhooks/

---

## ✅ Configuration Summary

| Item | Value | Location |
|------|-------|----------|
| **Website** | https://smart-home-bakery-platform.vercel.app | Razorpay account |
| **Login Required** | No (guest checkout enabled) | paymentService.js |
| **Test Key** | rzp_test_1DP5mmOlF5G5ag | .env files |
| **Payment Methods** | UPI, Card, Netbanking, Wallet | paymentService.js |
| **Plan Price** | ₹299/month (customizable) | payments.py |
| **Currency** | INR (Indian Rupees) | paymentService.js |
| **Free Plan** | ₹0 (No payment needed) | payments.py |

---

**You're all set! Start accepting payments today!** 🎉
