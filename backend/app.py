"""
Smart Home Bakery Management Platform - Flask Application
Main entry point for the backend API
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import config
from models.database import db, User, Recipe, Order, Ingredient
from services.ai_service import AIService
from utils.helpers import api_response


def create_app(config_name=None):
    """
    Application factory function
    
    Args:
        config_name: Configuration name ('development', 'testing', 'production')
    
    Returns:
        Flask application instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}})
    
    # Create uploads folder if not exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Context processors
    register_context_processors(app)
    
    # CLI commands
    register_cli_commands(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        # Seed database if needed
        seed_database()
    
    return app


def register_blueprints(app):
    """Register Flask blueprints (API routes)"""
    # Import routes
    from routes.auth import auth_bp
    from routes.recipes import recipes_bp
    from routes.ingredients import ingredients_bp
    from routes.orders import orders_bp
    from routes.dashboard import dashboard_bp
    from routes.ai import ai_bp
    from routes.expenses import expenses_bp
    from routes.market_rates import market_rates_bp
    from routes.payments import payments_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(recipes_bp, url_prefix='/api/recipes')
    app.register_blueprint(ingredients_bp, url_prefix='/api/ingredients')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(expenses_bp, url_prefix='/api/expenses')
    app.register_blueprint(market_rates_bp, url_prefix='/api/market-rates')
    app.register_blueprint(payments_bp, url_prefix='/api/payments')
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return api_response(message="Smart Home Bakery API is running!")
    
    @app.route('/', methods=['GET'])
    def index():
        """API documentation"""
        return jsonify({
            "name": "Smart Home Bakery Management Platform",
            "version": "1.0.0",
            "description": "AI-powered cake recipe and bakery management platform",
            "endpoints": {
                "health": "/api/health",
                "auth": "/api/auth",
                "recipes": "/api/recipes",
                "ingredients": "/api/ingredients",
                "orders": "/api/orders",
                "dashboard": "/api/dashboard",
                "ai": "/api/ai",
                "expenses": "/api/expenses",
                "market_rates": "/api/market-rates"
            }
        })


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return api_response(
            status="error",
            message="Resource not found",
            code=404
        )
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return api_response(
            status="error",
            message="Internal server error",
            code=500
        )
    
    @app.errorhandler(403)
    def forbidden(error):
        return api_response(
            status="error",
            message="Access forbidden",
            code=403
        )
    
    @app.errorhandler(400)
    def bad_request(error):
        return api_response(
            status="error",
            message="Bad request",
            code=400
        )


def register_context_processors(app):
    """Register context processors"""
    @app.before_request
    def before_request():
        """Execute before each request"""
        pass
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Execute after each request"""
        pass


def register_cli_commands(app):
    """Register Flask CLI commands"""
    
    @app.cli.command()
    def init_db():
        """Initialize database"""
        db.create_all()
        print("Database initialized!")
    
    @app.cli.command()
    def seed_db():
        """Seed database with sample data"""
        seed_database()
        print("Database seeded!")
    
    @app.cli.command()
    def drop_db():
        """Drop all database tables"""
        db.drop_all()
        print("Database dropped!")


def seed_database():
    """Seed database with sample data"""
    # Check if data already exists
    if User.query.first() is not None:
        return  # Data already exists
    
    try:
        # Create sample user
        sample_user = User(
            username='demo_baker',
            email='demo@bakery.local',
            password_hash='hashed_password',  # In production, hash the password
            full_name='Demo Baker',
            phone='9876543210',
            location='Bangalore',
            bakery_name='My Home Bakery',
            business_status='hobby'
        )
        db.session.add(sample_user)
        db.session.commit()
        
        print("Database seeded with sample data!")
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        db.session.rollback()


# Create app instance for development
if __name__ == '__main__':
    app = create_app()
    
    # Run development server
    app.run(
        host=app.config.get('SERVER_HOST', '0.0.0.0'),
        port=app.config.get('SERVER_PORT', 5000),
        debug=app.config.get('DEBUG', True)
    )

# Create the app instance for Gunicorn
app = create_app()
