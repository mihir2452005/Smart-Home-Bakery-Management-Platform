# Database Schema

## Tables Overview

### Users Table
Stores information about home bakers.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    location TEXT,
    bakery_name TEXT,
    business_status TEXT DEFAULT 'hobby', -- 'hobby' or 'professional'
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Recipes Table
Stores cake recipes (AI-generated or user-created).

```sql
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY,
    name TEXT NOT NULL,
    cake_type TEXT NOT NULL,
    weight TEXT NOT NULL, -- '500g', '1kg', '2kg', '3kg'
    servings INTEGER,
    is_eggless BOOLEAN,
    baking_temp INTEGER,
    baking_time INTEGER,
    tin_size TEXT,
    difficulty_level TEXT,
    ai_generated BOOLEAN,
    rating FLOAT,
    times_made INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Recipe Instructions Table
Step-by-step baking instructions.

```sql
CREATE TABLE recipe_instructions (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER NOT NULL FOREIGN KEY,
    step_number INTEGER NOT NULL,
    instruction TEXT NOT NULL,
    duration_minutes INTEGER,
    created_at TIMESTAMP
);
```

### Ingredients Table
Inventory management for bakers.

```sql
CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    category TEXT NOT NULL,
    price_per_unit FLOAT NOT NULL,
    total_quantity FLOAT NOT NULL,
    stock_quantity FLOAT NOT NULL,
    min_stock_alert FLOAT,
    last_purchased_date DATE,
    supplier TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Recipe Ingredients Table
Maps ingredients to recipes.

```sql
CREATE TABLE recipe_ingredients (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER NOT NULL FOREIGN KEY,
    ingredient_id INTEGER NOT NULL FOREIGN KEY,
    quantity FLOAT NOT NULL,
    unit TEXT NOT NULL,
    is_optional BOOLEAN,
    created_at TIMESTAMP
);
```

### Orders Table
Customer orders for cakes.

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY,
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
    status TEXT DEFAULT 'pending',
    estimated_ingredient_cost FLOAT,
    actual_cost FLOAT,
    selling_price FLOAT,
    actual_profit FLOAT,
    notes TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Order Items Table
Detailed breakdown of ingredients used in orders.

```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL FOREIGN KEY,
    ingredient_id INTEGER NOT NULL FOREIGN KEY,
    quantity_used FLOAT NOT NULL,
    unit TEXT NOT NULL,
    cost FLOAT NOT NULL,
    created_at TIMESTAMP
);
```

### Expenses Table
Business expense tracking.

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY,
    category TEXT NOT NULL,
    amount FLOAT NOT NULL,
    description TEXT,
    expense_date DATE NOT NULL,
    payment_method TEXT,
    receipt_url TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**Expense Categories:**
- ingredients
- equipment
- packaging
- utilities
- marketing
- other

### Profit Reports Table
Daily/monthly analytics and reports.

```sql
CREATE TABLE profit_reports (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY,
    report_date DATE NOT NULL,
    total_orders INTEGER,
    total_revenue FLOAT,
    total_ingredients_cost FLOAT,
    total_expenses FLOAT,
    total_profit FLOAT,
    average_profit_per_cake FLOAT,
    most_profitable_flavor TEXT,
    most_selling_flavor TEXT,
    created_at TIMESTAMP
);
```

### Bakery Market Rates Table
Competitor pricing analysis.

```sql
CREATE TABLE bakery_market_rates (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY,
    location TEXT NOT NULL,
    bakery_name TEXT,
    bakery_url TEXT,
    cake_type TEXT NOT NULL,
    weight TEXT,
    price FLOAT NOT NULL,
    currency TEXT DEFAULT 'INR',
    last_updated DATE,
    notes TEXT,
    created_at TIMESTAMP
);
```

### Decoration References Table
Pinterest/Instagram style decoration references.

```sql
CREATE TABLE decoration_references (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY,
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
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### AI Generated Images Table
Track AI image generations.

```sql
CREATE TABLE ai_generated_images (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY,
    prompt TEXT NOT NULL,
    image_url TEXT,
    ai_provider TEXT NOT NULL,
    model_used TEXT,
    usage_tokens INTEGER,
    cost FLOAT,
    created_at TIMESTAMP
);
```

### Inventory Alerts Table
Low stock notifications.

```sql
CREATE TABLE inventory_alerts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY,
    ingredient_id INTEGER NOT NULL FOREIGN KEY,
    alert_type TEXT NOT NULL,
    message TEXT,
    is_resolved BOOLEAN,
    created_at TIMESTAMP,
    resolved_at TIMESTAMP
);
```

### Baking Mistakes Table
Common baking problems and solutions.

```sql
CREATE TABLE baking_mistakes (
    id INTEGER PRIMARY KEY,
    problem TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    solutions TEXT NOT NULL,
    prevention_tips TEXT,
    affected_cake_types TEXT,
    is_verified BOOLEAN,
    created_at TIMESTAMP
);
```

### User Preferences Table
User app settings.

```sql
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE FOREIGN KEY,
    theme TEXT DEFAULT 'light',
    language TEXT DEFAULT 'en',
    currency TEXT DEFAULT 'INR',
    notification_email BOOLEAN DEFAULT 1,
    notification_sms BOOLEAN DEFAULT 0,
    auto_low_stock_alert BOOLEAN DEFAULT 1,
    weekly_profit_report BOOLEAN DEFAULT 1,
    preferred_ai_provider TEXT DEFAULT 'openai',
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Feedback Table
User ratings and reviews.

```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY,
    recipe_id INTEGER FOREIGN KEY,
    order_id INTEGER FOREIGN KEY,
    rating INTEGER,
    comment TEXT,
    category TEXT,
    created_at TIMESTAMP
);
```

## Relationships

```
users (1) ──── (N) recipes
users (1) ──── (N) ingredients
users (1) ──── (N) orders
users (1) ──── (N) expenses
users (1) ──── (N) profit_reports
users (1) ──── (N) bakery_market_rates
users (1) ──── (1) user_preferences

recipes (1) ──── (N) recipe_instructions
recipes (1) ──── (N) recipe_ingredients

ingredients (1) ──── (N) recipe_ingredients
ingredients (1) ──── (N) order_items
ingredients (1) ──── (N) inventory_alerts

orders (1) ──── (N) order_items
```

## Indexes

Created for performance optimization:

```sql
CREATE INDEX idx_recipes_user_id ON recipes(user_id);
CREATE INDEX idx_recipes_cake_type ON recipes(cake_type);
CREATE INDEX idx_ingredients_user_id ON ingredients(user_id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_expenses_user_id ON expenses(user_id);
CREATE INDEX idx_profit_reports_user_id ON profit_reports(user_id);
CREATE INDEX idx_bakery_rates_location ON bakery_market_rates(location);
```

## Sample Data

### Sample User
```json
{
  "username": "priya_baker",
  "email": "priya@example.com",
  "password_hash": "hashed_password",
  "full_name": "Priya Sharma",
  "phone": "9876543210",
  "location": "Bangalore",
  "bakery_name": "Priya's Home Bakery",
  "business_status": "professional"
}
```

### Sample Recipe
```json
{
  "user_id": 1,
  "name": "Eggless Chocolate Cake",
  "cake_type": "Chocolate",
  "weight": "1kg",
  "servings": 8,
  "is_eggless": true,
  "baking_temp": 180,
  "baking_time": 35,
  "tin_size": "8 inch round",
  "difficulty_level": "easy"
}
```

### Sample Order
```json
{
  "user_id": 1,
  "customer_name": "Anita Singh",
  "customer_phone": "9123456789",
  "cake_type": "Truffle",
  "cake_weight": "1kg",
  "flavor": "Dark Chocolate",
  "theme": "Anniversary",
  "budget": 1000,
  "order_date": "2024-01-01",
  "delivery_date": "2024-01-05"
}
```

## Migrations

For production with PostgreSQL:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

**Database size optimization note:** Consider archiving old orders and expenses monthly to keep database lean.
