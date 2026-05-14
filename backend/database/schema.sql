-- Smart Home Bakery Management Platform - Database Schema
-- SQLite Database for storing recipes, ingredients, orders, and analytics

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    location TEXT,
    bakery_name TEXT,
    business_status TEXT DEFAULT 'hobby', -- 'hobby' or 'professional'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recipes Table
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    cake_type TEXT NOT NULL,
    weight TEXT NOT NULL, -- '500g', '1kg', '2kg', '3kg'
    servings INTEGER,
    is_eggless BOOLEAN DEFAULT 0,
    baking_temp INTEGER, -- in Celsius
    baking_time INTEGER, -- in minutes
    tin_size TEXT,
    description TEXT,
    difficulty_level TEXT DEFAULT 'medium', -- 'easy', 'medium', 'hard'
    ai_generated BOOLEAN DEFAULT 1,
    image_url TEXT,
    rating FLOAT DEFAULT 0,
    times_made INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Recipe Instructions Table
CREATE TABLE IF NOT EXISTS recipe_instructions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    step_number INTEGER NOT NULL,
    instruction TEXT NOT NULL,
    duration_minutes INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Ingredients Table
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    unit TEXT NOT NULL, -- 'grams', 'ml', 'teaspoon', 'tablespoon', 'cups', 'litre'
    category TEXT NOT NULL, -- 'flour', 'sugar', 'butter', 'eggs', 'milk', 'chocolate', 'spices', etc.
    price_per_unit FLOAT NOT NULL,
    total_quantity FLOAT NOT NULL, -- total quantity purchased
    stock_quantity FLOAT NOT NULL, -- current stock
    min_stock_alert FLOAT,
    last_purchased_date DATE,
    supplier TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Recipe Ingredients Mapping
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity FLOAT NOT NULL,
    unit TEXT NOT NULL,
    is_optional BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    customer_name TEXT NOT NULL,
    customer_phone TEXT,
    customer_email TEXT,
    cake_type TEXT NOT NULL,
    cake_weight TEXT,
    flavor TEXT,
    theme TEXT,
    budget FLOAT,
    special_requirements TEXT,
    order_date DATE NOT NULL,
    delivery_date DATE NOT NULL,
    status TEXT DEFAULT 'pending', -- 'pending', 'accepted', 'in_progress', 'completed', 'cancelled'
    estimated_ingredient_cost FLOAT,
    decoration_difficulty TEXT,
    time_required_hours FLOAT,
    estimated_profit FLOAT,
    actual_cost FLOAT,
    selling_price FLOAT,
    actual_profit FLOAT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Order Items (detailed breakdown)
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity_used FLOAT NOT NULL,
    unit TEXT NOT NULL,
    cost FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);

-- Expenses Table
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL, -- 'ingredients', 'equipment', 'packaging', 'utilities', 'marketing', 'other'
    amount FLOAT NOT NULL,
    description TEXT,
    expense_date DATE NOT NULL,
    payment_method TEXT, -- 'cash', 'card', 'online', 'check'
    receipt_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Profit Reports Table
CREATE TABLE IF NOT EXISTS profit_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    report_date DATE NOT NULL,
    total_orders INTEGER,
    total_revenue FLOAT,
    total_ingredients_cost FLOAT,
    total_expenses FLOAT,
    total_profit FLOAT,
    average_profit_per_cake FLOAT,
    most_profitable_flavor TEXT,
    most_selling_flavor TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Bakery Market Rates Table
CREATE TABLE IF NOT EXISTS bakery_market_rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    location TEXT NOT NULL,
    bakery_name TEXT,
    bakery_url TEXT,
    cake_type TEXT NOT NULL,
    weight TEXT,
    price FLOAT NOT NULL,
    currency TEXT DEFAULT 'INR',
    last_updated DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Decoration References Table
CREATE TABLE IF NOT EXISTS decoration_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    cake_weight TEXT,
    style TEXT NOT NULL,
    image_url TEXT,
    source TEXT, -- 'pinterest', 'instagram', 'custom'
    cream_quantity_grams INTEGER,
    piping_style TEXT,
    drip_design TEXT,
    flower_quantity INTEGER,
    fondant_usage TEXT,
    difficulty_level TEXT,
    estimated_time_hours FLOAT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- AI Image Generations Table
CREATE TABLE IF NOT EXISTS ai_generated_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    prompt TEXT NOT NULL,
    image_url TEXT,
    ai_provider TEXT NOT NULL, -- 'openai', 'gemini'
    model_used TEXT,
    usage_tokens INTEGER,
    cost FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Inventory Alerts Table
CREATE TABLE IF NOT EXISTS inventory_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    alert_type TEXT NOT NULL, -- 'low_stock', 'out_of_stock', 'expiring_soon'
    message TEXT,
    is_resolved BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);

-- Baking Mistakes & Solutions Table
CREATE TABLE IF NOT EXISTS baking_mistakes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    solutions TEXT NOT NULL, -- JSON format with multiple solutions
    prevention_tips TEXT,
    affected_cake_types TEXT, -- JSON array
    is_verified BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Preferences Table
CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    theme TEXT DEFAULT 'light', -- 'light', 'dark'
    language TEXT DEFAULT 'en',
    currency TEXT DEFAULT 'INR',
    notification_email BOOLEAN DEFAULT 1,
    notification_sms BOOLEAN DEFAULT 0,
    auto_low_stock_alert BOOLEAN DEFAULT 1,
    weekly_profit_report BOOLEAN DEFAULT 1,
    preferred_ai_provider TEXT DEFAULT 'openai', -- 'openai', 'gemini'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Feedback & Ratings Table
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER,
    order_id INTEGER,
    rating INTEGER, -- 1-5
    comment TEXT,
    category TEXT, -- 'recipe_accuracy', 'cost_calculation', 'ai_recommendation', 'ui_ux', 'other'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Create Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_recipes_user_id ON recipes(user_id);
CREATE INDEX IF NOT EXISTS idx_recipes_cake_type ON recipes(cake_type);
CREATE INDEX IF NOT EXISTS idx_ingredients_user_id ON ingredients(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id);
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(expense_date);
CREATE INDEX IF NOT EXISTS idx_profit_reports_user_id ON profit_reports(user_id);
CREATE INDEX IF NOT EXISTS idx_profit_reports_date ON profit_reports(report_date);
CREATE INDEX IF NOT EXISTS idx_bakery_rates_location ON bakery_market_rates(location);
CREATE INDEX IF NOT EXISTS idx_bakery_rates_cake_type ON bakery_market_rates(cake_type);
