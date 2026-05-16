// Payment Service - Razorpay Integration
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

// Initiate payment
export const initiatePayment = async (planDetails) => {
  try {
    // Load Razorpay script
    await loadRazorpayScript();

    // Create order on backend
    const response = await fetch(`${API_URL}/api/payments/create-order`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        plan: planDetails.plan,
        amount: planDetails.amount,
        description: planDetails.description,
        email: planDetails.email,
        phone: planDetails.phone,
      }),
    });

    const data = await response.json();

    if (!data.success) {
      throw new Error(data.message || 'Failed to create order');
    }

    // Razorpay payment options
    const options = {
      key: process.env.REACT_APP_RAZORPAY_KEY || 'rzp_test_1DP5mmOlF5G5ag',
      amount: data.amount,
      currency: 'INR',
      name: 'Cake Hub',
      description: planDetails.description,
      order_id: data.orderId,
      image: '/cake-logo.png',
      prefill: {
        name: planDetails.name,
        email: planDetails.email,
        contact: planDetails.phone,
      },
      notes: {
        plan: planDetails.plan,
        userId: planDetails.userId,
      },
      theme: {
        color: '#ec4899', // Pink color
      },
      method: {
        upi: true,
        card: true,
        netbanking: true,
        wallet: true,
      },
      handler: async (response) => {
        // Verify payment on backend
        const verifyResponse = await fetch(`${API_URL}/api/payments/verify`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            razorpay_order_id: response.razorpay_order_id,
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_signature: response.razorpay_signature,
            userId: planDetails.userId,
            plan: planDetails.plan,
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
