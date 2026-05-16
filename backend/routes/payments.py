"""
Payment routes - Razorpay UPI integration for subscription management
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import os
import hmac
import hashlib
import json
from models.database import db, User, Subscription
from utils.helpers import api_response, require_json
import requests

payments_bp = Blueprint('payments', __name__, url_prefix='/api/payments')

# Razorpay configuration
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_1DP5mmOlF5G5ag')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'test_secret_key')

# Plan details
PLANS = {
    'hobby': {
        'amount': 0,  # Free
        'name': 'Hobby Baker',
        'features': [
            '10 Recipe Generations',
            'Cost Calculator',
            'Basic Analytics'
        ],
        'recipe_limit': 10,
        'duration_days': 30
    },
    'professional': {
        'amount': 29900,  # ₹299 in paise (Razorpay uses paise)
        'name': 'Professional',
        'features': [
            'Unlimited Recipes',
            'Full Analytics',
            'Market Analysis',
            'Priority Support'
        ],
        'recipe_limit': None,  # Unlimited
        'duration_days': 30
    },
    'enterprise': {
        'amount': 0,  # Custom
        'name': 'Enterprise',
        'features': [
            'Everything in Pro',
            'Custom Integration',
            'Dedicated Support'
        ],
        'recipe_limit': None,
        'duration_days': 365
    }
}


@payments_bp.route('/create-order', methods=['POST'])
@require_json
def create_order():
    """Create Razorpay order for payment"""
    try:
        data = request.get_json()
        plan = data.get('plan', 'professional')
        
        if plan not in PLANS:
            return api_response(
                status='error',
                message='Invalid plan',
                code=400
            )
        
        plan_info = PLANS[plan]
        amount = data.get('amount', plan_info['amount'])
        
        # Only create order if amount > 0 (paid plans)
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
        
        # Prepare Razorpay order request
        razorpay_order_data = {
            'amount': amount,  # Amount in paise
            'currency': 'INR',
            'receipt': f"receipt_{plan}_{datetime.now().timestamp()}",
            'description': f"Cake Hub - {plan_info['name']} Plan",
            'notes': {
                'plan': plan,
                'email': data.get('email'),
            }
        }
        
        # Create order via Razorpay API
        response = requests.post(
            'https://api.razorpay.com/v1/orders',
            auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET),
            data=razorpay_order_data
        )
        
        if response.status_code != 200:
            return api_response(
                status='error',
                message='Failed to create payment order',
                code=500
            )
        
        order = response.json()
        
        return api_response(
            status='success',
            data={
                'orderId': order['id'],
                'amount': order['amount'],
                'currency': order['currency'],
                'plan': plan
            }
        )
    
    except Exception as e:
        return api_response(
            status='error',
            message=f'Order creation failed: {str(e)}',
            code=500
        )


@payments_bp.route('/verify', methods=['POST'])
@require_json
def verify_payment():
    """Verify Razorpay payment signature"""
    try:
        data = request.get_json()
        
        # Get payment details
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        user_id = data.get('userId')
        plan = data.get('plan', 'professional')
        
        # Verify signature
        message = f"{razorpay_order_id}|{razorpay_payment_id}"
        generated_signature = hmac.new(
            RAZORPAY_KEY_SECRET.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if generated_signature != razorpay_signature:
            return api_response(
                status='error',
                message='Invalid payment signature',
                code=400
            )
        
        # Get user
        user = User.query.get(user_id)
        if not user:
            return api_response(
                status='error',
                message='User not found',
                code=404
            )
        
        # Create/update subscription
        plan_info = PLANS.get(plan, PLANS['professional'])
        expiry_date = datetime.utcnow() + timedelta(days=plan_info['duration_days'])
        
        subscription = Subscription.query.filter_by(user_id=user_id).first()
        
        if subscription:
            subscription.plan = plan
            subscription.status = 'active'
            subscription.expiry_date = expiry_date
            subscription.razorpay_payment_id = razorpay_payment_id
            subscription.updated_at = datetime.utcnow()
        else:
            subscription = Subscription(
                user_id=user_id,
                plan=plan,
                status='active',
                start_date=datetime.utcnow(),
                expiry_date=expiry_date,
                razorpay_payment_id=razorpay_payment_id
            )
            db.session.add(subscription)
        
        db.session.commit()
        
        return api_response(
            status='success',
            message='Payment verified successfully!',
            data={
                'plan': plan,
                'expiry_date': expiry_date.isoformat(),
                'status': 'active'
            }
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status='error',
            message=f'Verification failed: {str(e)}',
            code=500
        )


@payments_bp.route('/free-signup', methods=['POST'])
@require_json
def free_signup():
    """Create free tier subscription"""
    try:
        data = request.get_json()
        user_id = data.get('userId')
        
        user = User.query.get(user_id)
        if not user:
            return api_response(
                status='error',
                message='User not found',
                code=404
            )
        
        # Create hobby (free) subscription
        plan_info = PLANS['hobby']
        expiry_date = datetime.utcnow() + timedelta(days=plan_info['duration_days'])
        
        subscription = Subscription.query.filter_by(user_id=user_id).first()
        
        if subscription:
            subscription.plan = 'hobby'
            subscription.status = 'active'
            subscription.expiry_date = expiry_date
            subscription.updated_at = datetime.utcnow()
        else:
            subscription = Subscription(
                user_id=user_id,
                plan='hobby',
                status='active',
                start_date=datetime.utcnow(),
                expiry_date=expiry_date
            )
            db.session.add(subscription)
        
        db.session.commit()
        
        return api_response(
            status='success',
            message='Free subscription created!',
            data={
                'plan': 'hobby',
                'expiry_date': expiry_date.isoformat(),
                'status': 'active',
                'features': plan_info['features']
            },
            code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status='error',
            message=f'Signup failed: {str(e)}',
            code=500
        )


@payments_bp.route('/subscription/<int:user_id>', methods=['GET'])
def get_subscription(user_id):
    """Get user's current subscription"""
    try:
        subscription = Subscription.query.filter_by(user_id=user_id).first()
        
        if not subscription:
            return api_response(
                status='error',
                message='No active subscription found',
                code=404
            )
        
        plan_info = PLANS.get(subscription.plan, {})
        
        return api_response(
            status='success',
            data={
                'plan': subscription.plan,
                'status': subscription.status,
                'expiry_date': subscription.expiry_date.isoformat(),
                'features': plan_info.get('features', []),
                'recipe_limit': plan_info.get('recipe_limit'),
            }
        )
    
    except Exception as e:
        return api_response(
            status='error',
            message=f'Failed to fetch subscription: {str(e)}',
            code=500
        )


@payments_bp.route('/plans', methods=['GET'])
def get_plans():
    """Get all available plans"""
    plans_data = {}
    for plan_key, plan_info in PLANS.items():
        plans_data[plan_key] = {
            'name': plan_info['name'],
            'amount': plan_info['amount'],
            'features': plan_info['features'],
            'duration_days': plan_info['duration_days'],
        }
    
    return api_response(
        status='success',
        data=plans_data
    )
