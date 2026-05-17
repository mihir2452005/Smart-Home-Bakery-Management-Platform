// Payment Service - Razorpay Integration
// Supports payments from logged-in users AND guest checkout
const API_URL = process.env.REACT_APP_API_URL || 'https://cake-backend.onrender.com';

// Load Razorpay script
export const loadRazorpayScript = () => {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.onload = () => resolve(true);
    script.onerror = () => reject(new Error('Failed to load Razorpay'));
    document.body.appendChild(script);
  });
};

// Get user context (from auth store or session)
const getUserContext = () => {
  try {
    // Try to get from localStorage first
    const userId = localStorage.getItem('userId');
    const userEmail = localStorage.getItem('userEmail');
    const userName = localStorage.getItem('userName');
    const userPhone = localStorage.getItem('userPhone');

    return {
      userId: userId || null,
      email: userEmail || '',
      name: userName || 'Guest User',
      phone: userPhone || '',
      isLoggedIn: !!userId,
    };
  } catch (error) {
    return {
      userId: null,
      email: '',
      name: 'Guest User',
      phone: '',
      isLoggedIn: false,
    };
  }
};

// Initiate payment (for both logged-in and guest users)
export const initiatePayment = async (planDetails) => {
  try {
    // Load Razorpay script
    await loadRazorpayScript();

    // Get user context
    const userContext = getUserContext();

    // Prepare plan data
    const planData = {
      plan: planDetails.plan,
      amount: planDetails.amount || 0,
      description: planDetails.description,
      email: planDetails.email || userContext.email,
      phone: planDetails.phone || userContext.phone,
      name: planDetails.name || userContext.name,
      userId: planDetails.userId || userContext.userId,
      isGuest: !userContext.isLoggedIn && !planDetails.userId,
    };

    // Create order on backend
    const response = await fetch(`${API_URL}/api/payments/create-order`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(planData),
    });

    const data = await response.json();

    if (!data.success && data.status !== 'success') {
      throw new Error(data.message || 'Failed to create order');
    }

    // For free plans, no payment needed
    if (data.amount === 0) {
      // Directly create free subscription
      const freeResponse = await fetch(`${API_URL}/api/payments/free-signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(planData),
      });
      return await freeResponse.json();
    }

    // Razorpay payment options
    const options = {
      key: process.env.REACT_APP_RAZORPAY_KEY || 'rzp_test_1DP5mmOlF5G5ag',
      amount: data.amount,
      currency: 'INR',
      name: 'Cake Hub - AI Bakery Platform',
      description: planDetails.description || `${planData.plan} Plan Subscription`,
      order_id: data.orderId,
      image: '/cake-logo.png',
      prefill: {
        name: planData.name,
        email: planData.email,
        contact: planData.phone,
      },
      notes: {
        plan: planData.plan,
        userId: planData.userId,
        isGuest: planData.isGuest,
        website: 'https://smart-home-bakery-platform.vercel.app',
      },
      theme: {
        color: '#ec4899', // Pink gradient color
      },
      method: {
        upi: true,      // UPI (Google Pay, PhonePe, Paytm, etc.)
        card: true,     // Debit/Credit Cards
        netbanking: true, // Internet Banking
        wallet: true,   // Digital Wallets (Paytm, Mobikwik, etc.)
      },
      handler: async (response) => {
        // Payment successful - verify on backend
        const verifyResponse = await fetch(`${API_URL}/api/payments/verify`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            razorpay_order_id: response.razorpay_order_id,
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_signature: response.razorpay_signature,
            userId: planData.userId,
            plan: planData.plan,
            email: planData.email,
            isGuest: planData.isGuest,
            website: 'https://smart-home-bakery-platform.vercel.app',
          }),
        });

        const verifyData = await verifyResponse.json();
        return verifyData;
      },
      modal: {
        ondismiss: () => {
          console.log('Payment window closed');
        },
      },
    };

    const rzp = new window.Razorpay(options);
    rzp.open();
  } catch (error) {
    console.error('Payment error:', error);
    throw error;
  }
};

// Free tier signup
export const signupFreeTier = async (userData) => {
  try {
    const response = await fetch(`${API_URL}/api/payments/free-signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...userData,
        plan: 'hobby',
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Signup error:', error);
    throw error;
  }
};
