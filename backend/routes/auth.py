"""
Authentication Routes
User registration and login
"""

from flask import Blueprint, request
from models.database import db, User, UserPreference
from utils.helpers import api_response, require_json, validate_inputs, Validators

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
@require_json
@validate_inputs(['username', 'email', 'password', 'full_name'])
def register():
    """
    Register new user
    
    Required fields:
    - username: Unique username
    - email: Valid email
    - password: Password
    - full_name: Full name
    """
    data = request.get_json()
    
    # Validate inputs
    if not Validators.validate_email(data.get('email')):
        return api_response(
            status="error",
            message="Invalid email format",
            code=400
        )
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return api_response(
            status="error",
            message="Username already exists",
            code=400
        )
    
    if User.query.filter_by(email=data['email']).first():
        return api_response(
            status="error",
            message="Email already registered",
            code=400
        )
    
    try:
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=data['password'],  # In production, hash the password
            full_name=data['full_name'],
            phone=data.get('phone'),
            location=data.get('location'),
            bakery_name=data.get('bakery_name'),
            business_status=data.get('business_status', 'hobby')
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Create user preferences
        preferences = UserPreference(user_id=user.id)
        db.session.add(preferences)
        db.session.commit()
        
        return api_response(
            status="success",
            message="Registration successful!",
            data={
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "bakery_name": user.bakery_name
            },
            code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Registration failed: {str(e)}",
            code=500
        )


@auth_bp.route('/login', methods=['POST'])
@require_json
@validate_inputs(['username', 'password'])
def login():
    """
    User login
    
    Required fields:
    - username: Username
    - password: Password
    """
    data = request.get_json()
    
    # In production, use proper session management and JWT
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or user.password_hash != data['password']:
        return api_response(
            status="error",
            message="Invalid username or password",
            code=401
        )
    
    return api_response(
        status="success",
        message="Login successful!",
        data={
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "bakery_name": user.bakery_name,
            "token": f"user-token-{user.id}"  # In production, generate JWT
        }
    )


@auth_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """Get user profile"""
    user = User.query.get(user_id)
    
    if not user:
        return api_response(
            status="error",
            message="User not found",
            code=404
        )
    
    preferences = UserPreference.query.filter_by(user_id=user_id).first()
    
    return api_response(
        status="success",
        data={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "location": user.location,
            "bakery_name": user.bakery_name,
            "business_status": user.business_status,
            "created_at": user.created_at.isoformat(),
            "preferences": {
                "theme": preferences.theme,
                "language": preferences.language,
                "currency": preferences.currency,
                "notification_email": preferences.notification_email
            } if preferences else {}
        }
    )


@auth_bp.route('/profile/<int:user_id>', methods=['PUT'])
@require_json
def update_profile(user_id):
    """Update user profile"""
    user = User.query.get(user_id)
    
    if not user:
        return api_response(
            status="error",
            message="User not found",
            code=404
        )
    
    data = request.get_json()
    
    # Update allowed fields
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'phone' in data:
        user.phone = data['phone']
    if 'location' in data:
        user.location = data['location']
    if 'bakery_name' in data:
        user.bakery_name = data['bakery_name']
    if 'business_status' in data:
        user.business_status = data['business_status']
    
    try:
        db.session.commit()
        return api_response(
            status="success",
            message="Profile updated successfully!",
            data={
                "id": user.id,
                "username": user.username,
                "bakery_name": user.bakery_name,
                "updated_at": user.updated_at.isoformat()
            }
        )
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Update failed: {str(e)}",
            code=500
        )


@auth_bp.route('/preferences/<int:user_id>', methods=['GET'])
def get_preferences(user_id):
    """Get user preferences"""
    preferences = UserPreference.query.filter_by(user_id=user_id).first()
    
    if not preferences:
        return api_response(
            status="error",
            message="Preferences not found",
            code=404
        )
    
    return api_response(
        status="success",
        data={
            "theme": preferences.theme,
            "language": preferences.language,
            "currency": preferences.currency,
            "notification_email": preferences.notification_email,
            "notification_sms": preferences.notification_sms,
            "auto_low_stock_alert": preferences.auto_low_stock_alert,
            "weekly_profit_report": preferences.weekly_profit_report,
            "preferred_ai_provider": preferences.preferred_ai_provider
        }
    )


@auth_bp.route('/preferences/<int:user_id>', methods=['PUT'])
@require_json
def update_preferences(user_id):
    """Update user preferences"""
    preferences = UserPreference.query.filter_by(user_id=user_id).first()
    
    if not preferences:
        return api_response(
            status="error",
            message="Preferences not found",
            code=404
        )
    
    data = request.get_json()
    
    # Update preferences
    if 'theme' in data:
        preferences.theme = data['theme']
    if 'language' in data:
        preferences.language = data['language']
    if 'currency' in data:
        preferences.currency = data['currency']
    if 'notification_email' in data:
        preferences.notification_email = data['notification_email']
    if 'notification_sms' in data:
        preferences.notification_sms = data['notification_sms']
    if 'auto_low_stock_alert' in data:
        preferences.auto_low_stock_alert = data['auto_low_stock_alert']
    if 'weekly_profit_report' in data:
        preferences.weekly_profit_report = data['weekly_profit_report']
    if 'preferred_ai_provider' in data:
        preferences.preferred_ai_provider = data['preferred_ai_provider']
    
    try:
        db.session.commit()
        return api_response(
            status="success",
            message="Preferences updated!"
        )
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Update failed: {str(e)}",
            code=500
        )
