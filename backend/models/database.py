"""
Database Models using SQLAlchemy ORM
Defines all database tables as Python classes
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class User(db.Model):
    """User Model - Represents a home baker"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(120))
    bakery_name = db.Column(db.String(120))
    business_status = db.Column(db.String(50), default='hobby')  # 'hobby' or 'professional'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recipes = db.relationship('Recipe', backref='baker', lazy=True, cascade='all, delete-orphan')
    ingredients = db.relationship('Ingredient', backref='baker', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='baker', lazy=True, cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='baker', lazy=True, cascade='all, delete-orphan')
    preferences = db.relationship('UserPreference', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Recipe(db.Model):
    """Recipe Model - Stores cake recipes"""
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    cake_type = db.Column(db.String(120), nullable=False)
    weight = db.Column(db.String(20), nullable=False)  # '500g', '1kg', '2kg', '3kg'
    servings = db.Column(db.Integer)
    is_eggless = db.Column(db.Boolean, default=False)
    baking_temp = db.Column(db.Integer)  # in Celsius
    baking_time = db.Column(db.Integer)  # in minutes
    tin_size = db.Column(db.String(50))
    description = db.Column(db.Text)
    difficulty_level = db.Column(db.String(50), default='medium')
    ai_generated = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(255))
    rating = db.Column(db.Float, default=0)
    times_made = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True, cascade='all, delete-orphan')
    instructions = db.relationship('RecipeInstruction', backref='recipe', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Recipe {self.name}>'


class RecipeInstruction(db.Model):
    """Recipe Instructions - Step-by-step baking instructions"""
    __tablename__ = 'recipe_instructions'
    
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    duration_minutes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Ingredient(db.Model):
    """Ingredient Model - Tracks inventory"""
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    unit = db.Column(db.String(50), nullable=False)  # 'grams', 'ml', 'teaspoon', etc.
    category = db.Column(db.String(50), nullable=False)  # 'flour', 'sugar', 'butter', etc.
    price_per_unit = db.Column(db.Float, nullable=False)
    total_quantity = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Float, nullable=False)
    min_stock_alert = db.Column(db.Float)
    last_purchased_date = db.Column(db.Date)
    supplier = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_cost_used(self, quantity_used):
        """Calculate cost of used quantity"""
        if self.total_quantity == 0:
            return 0
        return (quantity_used / self.total_quantity) * (self.price_per_unit * self.total_quantity)


class RecipeIngredient(db.Model):
    """Recipe Ingredients - Mapping of ingredients to recipes"""
    __tablename__ = 'recipe_ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    is_optional = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    ingredient = db.relationship('Ingredient', backref='recipes')


class Order(db.Model):
    """Order Model - Customer orders"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20))
    customer_email = db.Column(db.String(120))
    cake_type = db.Column(db.String(120), nullable=False)
    cake_weight = db.Column(db.String(20))
    flavor = db.Column(db.String(120))
    theme = db.Column(db.String(120))
    budget = db.Column(db.Float)
    special_requirements = db.Column(db.Text)
    order_date = db.Column(db.Date, nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='pending')
    estimated_ingredient_cost = db.Column(db.Float)
    decoration_difficulty = db.Column(db.String(50))
    time_required_hours = db.Column(db.Float)
    estimated_profit = db.Column(db.Float)
    actual_cost = db.Column(db.Float)
    selling_price = db.Column(db.Float)
    actual_profit = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def calculate_profit(self):
        """Calculate actual profit"""
        if self.actual_cost and self.selling_price:
            self.actual_profit = self.selling_price - self.actual_cost
            return self.actual_profit
        return 0


class OrderItem(db.Model):
    """Order Items - Detailed breakdown of ingredients used"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    quantity_used = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Expense(db.Model):
    """Expense Model - Tracks all business expenses"""
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'ingredients', 'equipment', etc.
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    expense_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(50))
    receipt_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProfitReport(db.Model):
    """Profit Report - Daily/monthly analytics"""
    __tablename__ = 'profit_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_date = db.Column(db.Date, nullable=False)
    total_orders = db.Column(db.Integer, default=0)
    total_revenue = db.Column(db.Float, default=0)
    total_ingredients_cost = db.Column(db.Float, default=0)
    total_expenses = db.Column(db.Float, default=0)
    total_profit = db.Column(db.Float, default=0)
    average_profit_per_cake = db.Column(db.Float, default=0)
    most_profitable_flavor = db.Column(db.String(120))
    most_selling_flavor = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class BakeryMarketRate(db.Model):
    """Bakery Market Rates - Nearby competitor pricing"""
    __tablename__ = 'bakery_market_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    bakery_name = db.Column(db.String(120))
    bakery_url = db.Column(db.String(255))
    cake_type = db.Column(db.String(120), nullable=False)
    weight = db.Column(db.String(20))
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='INR')
    last_updated = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DecorationReference(db.Model):
    """Decoration Reference - Pinterest/Instagram style references"""
    __tablename__ = 'decoration_references'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cake_weight = db.Column(db.String(20))
    style = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(255))
    source = db.Column(db.String(50))  # 'pinterest', 'instagram', 'custom'
    cream_quantity_grams = db.Column(db.Integer)
    piping_style = db.Column(db.String(120))
    drip_design = db.Column(db.String(120))
    flower_quantity = db.Column(db.Integer)
    fondant_usage = db.Column(db.String(120))
    difficulty_level = db.Column(db.String(50))
    estimated_time_hours = db.Column(db.Float)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AIGeneratedImage(db.Model):
    """AI Generated Images - Track AI image generations"""
    __tablename__ = 'ai_generated_images'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    ai_provider = db.Column(db.String(50), nullable=False)  # 'openai', 'gemini'
    model_used = db.Column(db.String(50))
    usage_tokens = db.Column(db.Integer)
    cost = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class InventoryAlert(db.Model):
    """Inventory Alerts - Low stock notifications"""
    __tablename__ = 'inventory_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # 'low_stock', 'out_of_stock'
    message = db.Column(db.Text)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)


class BakingMistake(db.Model):
    """Baking Mistakes - Common issues and solutions"""
    __tablename__ = 'baking_mistakes'
    
    id = db.Column(db.Integer, primary_key=True)
    problem = db.Column(db.String(120), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    solutions = db.Column(db.Text, nullable=False)  # JSON format
    prevention_tips = db.Column(db.Text)
    affected_cake_types = db.Column(db.Text)  # JSON array
    is_verified = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserPreference(db.Model):
    """User Preferences - App settings"""
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    theme = db.Column(db.String(20), default='light')  # 'light', 'dark'
    language = db.Column(db.String(10), default='en')
    currency = db.Column(db.String(10), default='INR')
    notification_email = db.Column(db.Boolean, default=True)
    notification_sms = db.Column(db.Boolean, default=False)
    auto_low_stock_alert = db.Column(db.Boolean, default=True)
    weekly_profit_report = db.Column(db.Boolean, default=True)
    preferred_ai_provider = db.Column(db.String(20), default='openai')  # 'openai', 'gemini'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Feedback(db.Model):
    """Feedback - User ratings and reviews"""
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    rating = db.Column(db.Integer)  # 1-5
    comment = db.Column(db.Text)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
