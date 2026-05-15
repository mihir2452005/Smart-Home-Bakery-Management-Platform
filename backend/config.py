"""
Smart Home Bakery Platform - Configuration
Handles all environment and application settings
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Flask Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///cake_bakery.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Server
    SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    
    # File Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))  # 16MB
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # API Rate Limiting
    RATELIMIT_STORAGE_URL = 'memory://'
    
    # Scraping
    SCRAPING_TIMEOUT = int(os.getenv('SCRAPING_TIMEOUT', 10))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    
    # AI Configuration
    AI_MODEL_TEMPERATURE = 0.7
    AI_MODEL_MAX_TOKENS = 2048
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Cake Categories
    CAKE_TYPES = [
        'Vanilla',
        'Chocolate',
        'Red Velvet',
        'Carrot',
        'Cheesecake',
        'Truffle',
        'Mousse',
        'Black Forest',
        'Lemon',
        'Strawberry',
        'Coffee',
        'Butter Cake',
        'Fruit Cake',
        'Eggless Vanilla',
        'Eggless Chocolate'
    ]
    
    # Cake Sizes
    CAKE_SIZES = {
        '500g': {'servings': 4, 'tins': 6},
        '1kg': {'servings': 8, 'tins': 8},
        '2kg': {'servings': 16, 'tins': 10},
        '3kg': {'servings': 24, 'tins': 12}
    }
    
    # Decoration Styles
    DECORATION_STYLES = [
        'Minimal',
        'Elegant',
        'Modern',
        'Vintage',
        'Trendy',
        'Designer',
        'Fondant',
        'Drip',
        'Naked',
        'Rustic'
    ]


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    # Enforce HTTPS in production
    PREFERRED_URL_SCHEME = 'https'
    # Add security headers
    PROPAGATE_EXCEPTIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    # Better error logging
    JSON_SORT_KEYS = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
