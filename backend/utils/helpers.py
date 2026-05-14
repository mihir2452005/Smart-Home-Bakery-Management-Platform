"""
Utility Functions - Helpers and common functions
"""

from functools import wraps
from flask import jsonify
from datetime import datetime


def api_response(status="success", message="", data=None, code=200):
    """
    Standard API response format
    
    Args:
        status: 'success' or 'error'
        message: Response message
        data: Response data
        code: HTTP status code
    
    Returns:
        JSON response
    """
    return jsonify({
        "status": status,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }), code


def require_json(f):
    """Decorator to check if request has JSON content type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request
        if not request.is_json:
            return api_response(
                status="error",
                message="Request must be JSON",
                code=400
            )
        return f(*args, **kwargs)
    return decorated_function


def validate_inputs(required_fields):
    """Decorator to validate required input fields"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            data = request.get_json() or {}
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return api_response(
                    status="error",
                    message=f"Missing required fields: {', '.join(missing_fields)}",
                    code=400
                )
            return f(*args, **kwargs)
        return decorated_function
    return decorator


class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number (Indian format)"""
        import re
        pattern = r'^[6-9]\d{9}$'  # Indian phone numbers
        return re.match(pattern, phone) is not None if phone else True
    
    @staticmethod
    def validate_cake_weight(weight):
        """Validate cake weight"""
        valid_weights = ['500g', '1kg', '2kg', '3kg']
        return weight in valid_weights
    
    @staticmethod
    def validate_positive_number(value):
        """Validate positive number"""
        try:
            num = float(value)
            return num > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_budget(budget):
        """Validate budget is positive"""
        return Validators.validate_positive_number(budget)
    
    @staticmethod
    def validate_cake_type(cake_type):
        """Validate cake type"""
        valid_types = [
            'Vanilla', 'Chocolate', 'Red Velvet', 'Carrot',
            'Cheesecake', 'Truffle', 'Mousse', 'Black Forest',
            'Lemon', 'Strawberry', 'Coffee', 'Butter Cake',
            'Fruit Cake', 'Eggless Vanilla', 'Eggless Chocolate'
        ]
        return cake_type in valid_types


class Helpers:
    """Helper functions"""
    
    @staticmethod
    def format_price(price, currency='INR'):
        """Format price for display"""
        if currency == 'INR':
            return f"₹{price:,.2f}"
        return f"{currency} {price:,.2f}"
    
    @staticmethod
    def format_date(date_obj):
        """Format date for display"""
        if isinstance(date_obj, str):
            return date_obj
        return date_obj.strftime('%d-%m-%Y')
    
    @staticmethod
    def get_profit_status(profit_margin):
        """Get profit margin status"""
        if profit_margin >= 50:
            return "Excellent"
        elif profit_margin >= 40:
            return "Good"
        elif profit_margin >= 30:
            return "Average"
        elif profit_margin >= 20:
            return "Fair"
        else:
            return "Poor"
    
    @staticmethod
    def calculate_monthly_projection(daily_profit, days_worked=25):
        """Calculate monthly profit projection"""
        return daily_profit * days_worked
    
    @staticmethod
    def get_cake_size_servings(weight):
        """Get number of servings based on cake weight"""
        servings_map = {
            '500g': 4,
            '1kg': 8,
            '2kg': 16,
            '3kg': 24
        }
        return servings_map.get(weight, 0)
    
    @staticmethod
    def get_cake_size_tin(weight):
        """Get tin size based on cake weight"""
        tin_map = {
            '500g': '6 inch round',
            '1kg': '8 inch round',
            '2kg': '10 inch round',
            '3kg': '12 inch round'
        }
        return tin_map.get(weight, 'Standard')
    
    @staticmethod
    def paginate_query(query, page, per_page=20):
        """
        Paginate database query
        
        Args:
            query: SQLAlchemy query
            page: Page number (1-indexed)
            per_page: Items per page
        
        Returns:
            Tuple of (items, total_count, total_pages)
        """
        total_count = query.count()
        total_pages = (total_count + per_page - 1) // per_page
        
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return items, total_count, total_pages
    
    @staticmethod
    def generate_pagination_data(items, total_count, total_pages, page, per_page=20):
        """Generate pagination metadata"""
        return {
            'items': items,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }
