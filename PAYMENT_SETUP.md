# UPI Payment Integration - Configuration Guide

## Overview
The Smart Home Bakery Management Platform now supports UPI payments through **Razorpay**, India's most popular payment gateway.

## ✅ What's Integrated

### Frontend
- **Payment Service**: `frontend/src/services/paymentService.js`
  - `loadRazorpayScript()` - Loads Razorpay SDK
  - `initiatePayment()` - Handles payment initiation
  - `signupFreeTier()` - Free tier signup

- **HomePage Payment Buttons**: `frontend/src/pages/HomePage.jsx`
  - "Get Started" button (Hobby - Free)
  - "Start Free Trial" button (Professional - ₹299/month)
  - "Contact Sales" button (Enterprise)

### Backend
- **Payment Routes**: `backend/routes/payments.py`
  - `POST /api/payments/create-order` - Create Razorpay order
  - `POST /api/payments/verify` - Verify payment signature
  - `POST /api/payments/free-signup` - Free tier signup
  - `GET /api/payments/subscription/<user_id>` - Get subscription info
  - `GET /api/payments/plans` - Get all available plans

- **Database Model**: `backend/models/database.py`
  - `Subscription` table - Stores user subscriptions and payment info

## 🔧 How to Edit/Configure UPI Settings

### 1. **Change Payment Plans/Prices**
**File**: `backend/routes/payments.py` (Lines 20-50)

```python
PLANS = {
    'hobby': {
        'amount': 0,  # Free (₹0)
        'name': 'Hobby Baker',
        'features': [...],
        'recipe_limit': 10,
        'duration_days': 30
    },
    'professional': {
        'amount': 29900,  # ₹299 in paise (Razorpay uses paise)
        'name': 'Professional',
        'features': [...],
        'recipe_limit': None,  # Unlimited
        'duration_days': 30
    },
    'enterprise': {
        'amount': 0,  # Custom pricing
        ...
    }
}
```

**To change prices:**
- Hobby: Change `'amount': 0` to desired amount in paise (1 Rupee = 100 paise)
- Professional: Change `'amount': 29900` (currently ₹299) to desired amount
- Example: For ₹499, use `'amount': 49900`

**To change plan features:**
- Edit the `'features'` array for each plan
- Edit `'recipe_limit'` for API rate limiting
- Edit `'duration_days'` for subscription length

---

### 2. **Update Razorpay Credentials**
**Files to update:**

#### Backend: `backend/routes/payments.py` (Lines 17-18)
```python
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_1DP5mmOlF5G5ag')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'test_secret_key')
```

#### Frontend: `frontend/src/services/paymentService.js` (Line 39)
```javascript
key: process.env.REACT_APP_RAZORPAY_KEY || 'rzp_test_1DP5mmOlF5G5ag',
```

**To set up real Razorpay account:**
1. Go to https://razorpay.com
2. Sign up for a merchant account
3. Get your API keys from Dashboard → Settings → API Keys
4. Copy `Key ID` and `Key Secret`
5. Set environment variables:
   - Backend: `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`
   - Frontend: `REACT_APP_RAZORPAY_KEY`

---

### 3. **Update Pricing Display in UI**
**File**: `frontend/src/pages/HomePage.jsx` (Lines 190-250)

```jsx
{/* Professional Plan Card */}
<div className="p-8 bg-white...">
  <h3 className="text-2xl font-bold...">Professional</h3>
  <p className="text-gray-600...">For growing businesses</p>
  <p className="text-4xl font-bold...">
    <span className="text-lg">₹</span>299<span className="text-lg">/mo</span>
  </p>
  {/* Update this price display */}
  <button onClick={() => handlePricingClick('professional')}>
    Start Free Trial
  </button>
  <ul className="space-y-3 text-left">
    <li>✓ Unlimited Recipes</li>
    <li>✓ Full Analytics</li>
    {/* Update features here */}
  </ul>
</div>
```

**To update pricing display:**
- Change `<span>₹</span>299<span>/mo</span>` to your new price
- Update features list as needed

---

### 4. **Supported Payment Methods**
**UPI Payment Options** (Enabled by default):

In `frontend/src/services/paymentService.js` (Line 62):
```javascript
method: {
  upi: true,        // ✅ UPI Direct
  card: true,       // ✅ Credit/Debit Cards
  netbanking: true, // ✅ Net Banking
  wallet: true,     // ✅ Digital Wallets
},
```

**To disable payment methods:**
- Set any to `false`
- Example: To allow only UPI: `{ upi: true, card: false, netbanking: false, wallet: false }`

---

### 5. **Update Company Branding**
**File**: `frontend/src/services/paymentService.js` (Lines 50-55)

```javascript
const options = {
  key: process.env.REACT_APP_RAZORPAY_KEY,
  amount: data.amount,
  currency: 'INR',
  name: 'Cake Hub',  // ← Update company name here
  description: planDetails.description,
  image: '/cake-logo.png',  // ← Update logo path here
  theme: {
    color: '#ec4899',  // ← Update primary color (pink)
  },
};
```

---

### 6. **Free Trial vs Paid Plans**
**File**: `backend/routes/payments.py` (Lines 54-60)

Currently, all plans except free can be customized:
```python
# Free plan (no payment needed)
if amount == 0:
    return api_response(
        status='success',
        data={
            'orderId': f"order_{plan}_{datetime.now().timestamp()}",
            'amount': 0,
            'plan': plan,
            'message': 'Free plan - no payment needed'
        }
    )
```

**To add free trial for Professional:**
1. In `PLANS['professional']`, add: `'trial_days': 7`
2. Modify backend logic to check for trial eligibility

---

### 7. **Email Notifications for Payments**
**File**: `backend/routes/payments.py` (Line 125)

After successful payment verification, add email notification:
```python
# Add this after subscription is created
send_payment_confirmation_email(
    user_email=user.email,
    plan=plan,
    expiry_date=expiry_date
)
```

---

### 8. **View Subscription Details**
**API Endpoint**: `GET /api/payments/subscription/{user_id}`

**Example Response**:
```json
{
  "status": "success",
  "data": {
    "plan": "professional",
    "status": "active",
    "expiry_date": "2026-06-16T12:00:00",
    "features": [
      "Unlimited Recipes",
      "Full Analytics",
      "Market Analysis",
      "Priority Support"
    ],
    "recipe_limit": null
  }
}
```

---

### 9. **Track Payment History**
**Database Table**: `subscriptions` table

Fields available:
- `user_id` - User who purchased
- `plan` - Plan name (hobby/professional/enterprise)
- `status` - Payment status (active/cancelled/expired)
- `start_date` - Subscription start date
- `expiry_date` - Subscription expiry date
- `razorpay_payment_id` - Razorpay payment reference
- `razorpay_order_id` - Razorpay order reference

---

### 10. **Environment Variables (.env)**

Add these to your `.env` files:

**Backend (.env)**:
```
RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_secret_key_here
```

**Frontend (.env)**:
```
REACT_APP_RAZORPAY_KEY=rzp_live_xxxxxxxxxxxxx
REACT_APP_API_URL=https://cake-backend.onrender.com
```

**Vercel Environment Variables** (for production):
1. Go to Vercel Dashboard → Project Settings → Environment Variables
2. Add `REACT_APP_RAZORPAY_KEY` and `REACT_APP_API_URL`

---

## 🧪 Testing Payments

### Test Razorpay Credentials
- **Key ID**: `rzp_test_1DP5mmOlF5G5ag`
- **Key Secret**: `test_secret_key`

### Test UPI Payment
1. Open pricing page
2. Click "Start Free Trial"
3. In Razorpay test gateway:
   - Use any test UPI ID: `success@razorpay`
   - Payment will succeed
   - Subscription will be created

---

## 📊 Common Customizations

| What | Where | How |
|------|-------|-----|
| Change price | `backend/routes/payments.py` PLANS dict | Update `'amount'` value |
| Add new plan | `backend/routes/payments.py` PLANS dict | Add new key with plan config |
| Update currency | `frontend/src/services/paymentService.js` | Change `currency: 'INR'` |
| Change payment gateway | `frontend/src/services/paymentService.js` | Replace Razorpay with Stripe/Square |
| Require payment verification | `backend/routes/payments.py` verify function | Strengthen signature validation |
| Auto-activate features | `backend/routes/payments.py` | Add feature activation logic |

---

## ⚠️ Important Notes

1. **Security**: Never commit real Razorpay keys - use environment variables
2. **Testing**: Use test credentials first before going live
3. **Currency**: Currently set to INR (Indian Rupees) - change if needed
4. **Subscription Duration**: Default 30 days - modify `duration_days` for custom periods
5. **User Data**: Payment info stored in `subscriptions` table - maintain backups

---

## 🚀 Next Steps

1. ✅ Get Razorpay merchant account
2. ✅ Add real API credentials to environment variables
3. ✅ Test payments with test credentials
4. ✅ Configure email notifications
5. ✅ Set up payment webhooks for advanced features
6. ✅ Monitor transactions in Razorpay dashboard

---

**Questions?** Check Razorpay docs: https://razorpay.com/docs/
