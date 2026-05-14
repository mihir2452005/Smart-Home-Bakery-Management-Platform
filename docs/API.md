# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication

All requests should include:
```
Authorization: Bearer <user-token>
Content-Type: application/json
```

## Response Format

### Success Response
```json
{
  "status": "success",
  "message": "Operation successful",
  "data": { ... },
  "timestamp": "2024-01-01T12:00:00"
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description",
  "data": null,
  "timestamp": "2024-01-01T12:00:00"
}
```

## Endpoints

### 🔐 Authentication

#### Register User
```
POST /auth/register
Content-Type: application/json

{
  "username": "baker1",
  "email": "baker@example.com",
  "password": "password123",
  "full_name": "John Baker",
  "phone": "9876543210",
  "location": "Bangalore",
  "bakery_name": "My Home Bakery",
  "business_status": "hobby"
}

Response: 201 Created
{
  "user_id": 1,
  "username": "baker1",
  "email": "baker@example.com"
}
```

#### Login
```
POST /auth/login

{
  "username": "baker1",
  "password": "password123"
}

Response: 200 OK
{
  "user_id": 1,
  "username": "baker1",
  "token": "user-token-1"
}
```

#### Get Profile
```
GET /auth/profile/{user_id}

Response: 200 OK
{
  "id": 1,
  "full_name": "John Baker",
  "email": "baker@example.com",
  "bakery_name": "My Home Bakery"
}
```

### 🎂 Recipes

#### Generate Recipe
```
POST /recipes/generate

{
  "user_id": 1,
  "cake_weight": "1kg",
  "flavor": "Chocolate",
  "budget": 500,
  "oven_type": "gas_oven",
  "servings": 8,
  "is_eggless": true
}

Response: 201 Created
{
  "recipe_id": 1,
  "name": "Chocolate Cake",
  "ingredients": [...],
  "instructions": [...],
  "baking_temp": 180,
  "baking_time": 35,
  "estimated_cost": 350
}
```

#### Get All Recipes
```
GET /recipes/{user_id}?page=1&per_page=20

Response: 200 OK
{
  "items": [...],
  "pagination": {
    "page": 1,
    "total_pages": 5,
    "has_next": true
  }
}
```

#### Get Recipe Details
```
GET /recipes/{recipe_id}

Response: 200 OK
{
  "id": 1,
  "name": "Chocolate Cake",
  "ingredients": [...],
  "instructions": [...],
  "rating": 4.5,
  "times_made": 3
}
```

#### Rate Recipe
```
POST /recipes/{recipe_id}/rate

{
  "rating": 5,
  "times_made": true
}

Response: 200 OK
{
  "rating": 4.8,
  "times_made": 4
}
```

### 📦 Ingredients

#### Add Ingredient
```
POST /ingredients

{
  "user_id": 1,
  "name": "All-purpose Flour",
  "category": "flour",
  "unit": "kg",
  "price_per_unit": 40,
  "total_quantity": 5,
  "min_stock_alert": 1,
  "supplier": "Local Store"
}

Response: 201 Created
{
  "id": 1,
  "name": "All-purpose Flour",
  "stock_quantity": 5
}
```

#### Get Ingredients
```
GET /ingredients/{user_id}?page=1&category=flour

Response: 200 OK
{
  "items": [
    {
      "id": 1,
      "name": "All-purpose Flour",
      "stock_quantity": 5,
      "price_per_unit": 40
    }
  ]
}
```

#### Use Ingredient
```
POST /ingredients/{ingredient_id}/use

{
  "quantity_used": 0.5
}

Response: 200 OK
{
  "quantity_used": 0.5,
  "cost_used": 20,
  "stock_remaining": 4.5
}
```

#### Get Low Stock Alerts
```
GET /ingredients/{user_id}/alerts

Response: 200 OK
{
  "alerts": [
    {
      "id": 1,
      "ingredient_name": "Butter",
      "alert_type": "low_stock",
      "message": "Butter stock is running low!"
    }
  ]
}
```

### 🛒 Orders

#### Create Order
```
POST /orders

{
  "user_id": 1,
  "customer_name": "Priya Sharma",
  "customer_phone": "9876543210",
  "customer_email": "priya@example.com",
  "cake_type": "Chocolate",
  "cake_weight": "1kg",
  "flavor": "Dark Chocolate",
  "theme": "Birthday",
  "budget": 800,
  "order_date": "2024-01-01",
  "delivery_date": "2024-01-05"
}

Response: 201 Created
{
  "order_id": 1,
  "customer_name": "Priya Sharma",
  "status": "pending"
}
```

#### Estimate Order Cost
```
POST /orders/{order_id}/estimate

{
  "ingredients": [
    {
      "ingredient_id": 1,
      "quantity_used": 0.3
    },
    {
      "ingredient_id": 2,
      "quantity_used": 0.2
    }
  ]
}

Response: 200 OK
{
  "estimated_ingredient_cost": 250,
  "suggested_selling_price": 650,
  "profit_margin": 61.5
}
```

#### Update Order Status
```
PUT /orders/{order_id}/status

{
  "status": "completed"
}

Response: 200 OK
{
  "order_id": 1,
  "status": "completed"
}
```

#### Finalize Order
```
POST /orders/{order_id}/finalize

{
  "selling_price": 700,
  "actual_cost": 250,
  "notes": "Customer very happy!"
}

Response: 200 OK
{
  "selling_price": 700,
  "actual_cost": 250,
  "profit": 450,
  "profit_margin": 64.3
}
```

### 📊 Dashboard

#### Get Summary
```
GET /dashboard/{user_id}/summary?days=30

Response: 200 OK
{
  "summary": {
    "total_orders": 5,
    "total_revenue": 3500,
    "total_profit": 2100,
    "average_profit_per_cake": 420,
    "most_selling_flavor": "Chocolate"
  },
  "profit_margin": 60
}
```

#### Generate Report
```
POST /dashboard/{user_id}/generate-report

Response: 200 OK
{
  "report_date": "2024-01-01",
  "total_orders": 3,
  "total_revenue": 2100,
  "total_profit": 1200
}
```

### 🤖 AI Features

#### Generate Recipe
```
POST /ai/recipe-generator

{
  "user_id": 1,
  "cake_weight": "1kg",
  "flavor": "Vanilla",
  "budget": 400,
  "oven_type": "gas_oven",
  "servings": 8
}
```

#### Get Decoration Recommendations
```
POST /ai/decoration-recommendations

{
  "user_id": 1,
  "cake_weight": "1kg",
  "style": "Elegant"
}

Response: 200 OK
{
  "cream_quantity_grams": 250,
  "piping_style": "French",
  "difficulty_level": "medium",
  "estimated_time_hours": 1.5
}
```

#### Diagnose Baking Mistake
```
POST /ai/diagnose-mistake

{
  "problem_description": "Cake sank in the middle",
  "cake_type": "Chocolate"
}

Response: 200 OK
{
  "likely_cause": "Oven temperature too high or insufficient baking time",
  "solutions": [
    "Reduce oven temperature by 10-15 degrees",
    "Increase baking time",
    "Use ice cream scoop for even batter distribution"
  ],
  "prevention_tips": [...]
}
```

#### Suggest Selling Price
```
POST /ai/suggest-price

{
  "total_cost": 250,
  "market_rate": 600,
  "desired_margin": 40
}

Response: 200 OK
{
  "suggested_price": 416.67,
  "profit": 166.67,
  "profit_margin": 40
}
```

### 💰 Expenses

#### Add Expense
```
POST /expenses

{
  "user_id": 1,
  "category": "ingredients",
  "amount": 1500,
  "description": "Flour, sugar, butter bulk purchase",
  "expense_date": "2024-01-01",
  "payment_method": "card"
}

Response: 201 Created
{
  "id": 1,
  "category": "ingredients",
  "amount": 1500
}
```

#### Get Expenses
```
GET /expenses/{user_id}?page=1&category=ingredients

Response: 200 OK
{
  "items": [...],
  "pagination": {...}
}
```

### 📈 Market Rates

#### Scrape Market Rates
```
POST /market-rates/scrape

{
  "user_id": 1,
  "location": "Bangalore",
  "cake_types": ["Chocolate", "Truffle", "Fondant"]
}

Response: 201 Created
{
  "rates_scraped": 15,
  "location": "Bangalore",
  "rates": [...]
}
```

#### Analyze Market
```
POST /market-rates/analyze/{user_id}

{
  "cake_type": "Chocolate",
  "weight": "1kg",
  "user_cake_cost": 250
}

Response: 200 OK
{
  "market_average": 500,
  "market_min": 400,
  "market_max": 700,
  "recommended_price": 500,
  "profit_at_market_average": 250,
  "competitive_analysis": {...}
}
```

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

## Rate Limiting

Recommended for production:
- 100 requests per 15 minutes per user
- 1000 requests per hour per API key

## Pagination

All list endpoints support pagination:
```
?page=1&per_page=20
```

Response includes:
```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_count": 100,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

---

**For more information, refer to the backend code and postman collection.**
