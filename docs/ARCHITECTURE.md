# Architecture & Development Guide

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  React Frontend (Port 3000)                               │  │
│  │  - Components: Layout, Dashboard, Pages                   │  │
│  │  - State Management: Zustand Store                        │  │
│  │  - Routing: React Router v6                               │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                    (REST API via Axios)
                              │
┌─────────────────────────────────────────────────────────────────┐
│                        API LAYER                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Flask Backend (Port 5000)                                │  │
│  │  - Routes: /api/auth, /recipes, /ingredients, etc.       │  │
│  │  - Blueprints: 8 route modules                            │  │
│  │  - Services: AI, Scraping, Calculation                    │  │
│  │  - Middleware: CORS, Error Handling, Auth                 │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
            (SQL Queries via SQLAlchemy ORM)
                              │
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Database Layer                                            │  │
│  │  - SQLite (Development): cake_bakery.db                   │  │
│  │  - PostgreSQL (Production)                                │  │
│  │  - Tables: Users, Recipes, Ingredients, Orders, etc.      │  │
│  │  - Relationships: Proper FK and indexes                   │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
        (External API Calls: OpenAI, Gemini, Web Scraping)
```

## Backend Architecture

### Folder Structure

```
backend/
├── app.py                  # Flask app factory
├── config.py              # Configuration management
├── models/
│   └── database.py       # SQLAlchemy ORM models (16 tables)
├── routes/               # API endpoints
│   ├── auth.py          # Authentication
│   ├── recipes.py       # Recipe management
│   ├── ingredients.py   # Inventory
│   ├── orders.py        # Order management
│   ├── dashboard.py     # Analytics
│   ├── ai.py            # AI features
│   ├── expenses.py      # Expense tracking
│   └── market_rates.py  # Market analysis
├── services/            # Business logic
│   ├── ai_service.py    # AI integration (OpenAI, Gemini)
│   ├── scraping_service.py  # Web scraping
│   └── calculation_service.py  # Cost calculations
├── utils/
│   └── helpers.py       # Utilities, validators, decorators
├── database/
│   └── schema.sql       # Database schema
└── requirements.txt     # Python dependencies
```

### Design Patterns

#### 1. Model-View-Controller (MVC)

- **Models:** SQLAlchemy ORM in `models/database.py`
- **Views:** JSON responses via Flask routes
- **Controllers:** Route handlers in `routes/` modules

#### 2. Service Layer

```python
# Separation of concerns
routes/recipes.py  →  services/ai_service.py  →  models/database.py
```

#### 3. Decorator Pattern

```python
@app.route('/api/recipes')
@api_response()  # Standardizes response format
@require_json()  # Validates JSON content-type
def get_recipes():
    return {"recipes": []}
```

#### 4. Factory Pattern

```python
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    return app
```

### Data Flow

```
Request Flow:
1. Client sends HTTP request to /api/recipes/generate
2. Flask routes request to recipes.py route handler
3. Handler validates input using validators
4. Calls AIService.generate_recipe()
5. AIService calls OpenAI API
6. Response is parsed and formatted
7. Recipe data inserted into database
8. Response wrapper applied via @api_response()
9. JSON response sent to client

Response Format:
{
  "status": "success",
  "message": "Recipe generated successfully",
  "data": {...},
  "timestamp": "2024-01-01T12:00:00"
}
```

---

## Frontend Architecture

### Folder Structure

```
frontend/
├── public/
│   └── index.html       # HTML entry point
├── src/
│   ├── App.jsx          # Main app component with routing
│   ├── App.css          # Global styles
│   ├── index.js         # React initialization
│   ├── index.css        # Tailwind imports
│   ├── components/
│   │   └── Layout.jsx   # Sidebar + Header
│   ├── pages/           # Page components
│   │   ├── LoginPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── RecipeGeneratorPage.jsx
│   │   └── ...
│   ├── services/
│   │   ├── api.js       # Axios API client
│   │   └── store.js     # Zustand global store
│   └── styles/          # CSS modules
├── package.json         # NPM dependencies
├── vite.config.js       # Build configuration
└── tailwind.config.js   # Tailwind configuration
```

### Component Architecture

```
App.jsx (Router)
├── Layout (Sidebar + Header)
│   ├── DashboardPage
│   ├── RecipeGeneratorPage
│   │   └── RecipeForm
│   │   └── RecipeResult
│   ├── InventoryPage
│   │   └── IngredientList
│   │   └── AddIngredientForm
│   └── ... other pages
└── AuthPages
    ├── LoginPage
    └── RegisterPage
```

### State Management (Zustand)

```javascript
// Global Store Structure
const store = {
  user: null,
  isLoggedIn: false,
  preferences: {...},
  recipes: [],
  selectedRecipe: null,
  orders: [],
  ingredients: [],
  dashboardData: {...},
  
  actions: {
    setUser,
    setPreferences,
    logout,
    setRecipes,
    setOrders,
    ...
  }
}

// Usage in Component
const { user, recipes, setRecipes } = useStore();
```

### API Client Organization

```javascript
// api.js structure
const apiClient = axios.create({...});

const authAPI = {
  register: async (data) => {...},
  login: async (data) => {...},
  getProfile: async (id) => {...},
};

const recipeAPI = {
  generateRecipe: async (data) => {...},
  getRecipes: async (userId) => {...},
  getRecipeById: async (id) => {...},
};

// Usage in components
const recipes = await recipeAPI.getRecipes(userId);
```

---

## Database Architecture

### Entity Relationship Diagram

```
users (1) ──── (N) recipes
users (1) ──── (N) ingredients
users (1) ──── (N) orders
users (1) ──── (N) expenses
users (1) ──── (1) user_preferences

recipes (1) ──── (N) recipe_instructions
recipes (1) ──── (N) recipe_ingredients

ingredients (1) ──── (N) recipe_ingredients
ingredients (1) ──── (N) order_items
ingredients (1) ──── (N) inventory_alerts

orders (1) ──── (N) order_items

users (1) ──── (N) profit_reports
users (1) ──── (N) bakery_market_rates
users (1) ──── (N) ai_generated_images
users (1) ──── (N) decoration_references
```

### Query Optimization

1. **Indexing Strategy:**
   - User ID (frequent WHERE clause)
   - Cake type (filtering)
   - Order status (filtering)
   - Dates (range queries)

2. **Query Patterns:**
   ```python
   # Avoid N+1 queries
   recipes = Recipe.query.filter_by(user_id=user_id).all()
   # Instead of:
   for recipe in recipes:
       ingredients = recipe.ingredients  # N queries!
   
   # Use eager loading:
   recipes = Recipe.query.options(
       joinedload(Recipe.ingredients)
   ).filter_by(user_id=user_id).all()
   ```

3. **Pagination:**
   ```python
   page = request.args.get('page', 1, type=int)
   per_page = request.args.get('per_page', 20, type=int)
   
   paginated = Recipe.query.filter_by(user_id=user_id)\
       .paginate(page=page, per_page=per_page)
   ```

---

## API Design

### RESTful Principles

```
GET    /api/recipes/{user_id}       # List recipes
POST   /api/recipes                 # Create recipe
GET    /api/recipes/{id}            # Get recipe details
PUT    /api/recipes/{id}            # Update recipe
DELETE /api/recipes/{id}            # Delete recipe
```

### Response Format

All responses follow standard format:

```json
{
  "status": "success|error",
  "message": "Human-readable message",
  "data": { /* actual data */ },
  "timestamp": "ISO-8601 timestamp"
}
```

### Error Handling

```python
# Consistent error responses
return api_response(
    status="error",
    message="Recipe not found",
    data=None,
    status_code=404
)
```

### Pagination

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

## Development Workflow

### Feature Development Steps

1. **Create branch:**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Update backend:**
   - Add database model if needed
   - Create service method
   - Add route handler
   - Test with Postman/curl

3. **Update frontend:**
   - Add API client method
   - Create/update component
   - Add state management
   - Test in browser

4. **Testing:**
   - Backend: `pytest`
   - Frontend: `npm test`

5. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/new-feature
   ```

6. **Create pull request**

### Coding Standards

#### Backend (Python)

```python
# Follow PEP 8
# Use type hints
def calculate_profit(revenue: float, cost: float) -> float:
    """Calculate profit with percentage."""
    profit = revenue - cost
    return profit

# Use docstrings
class RecipeService:
    """Handles recipe-related business logic."""
    
    @staticmethod
    def generate_recipe(cake_weight: str) -> dict:
        """Generate AI recipe for given cake weight."""
        pass
```

#### Frontend (React/JavaScript)

```javascript
// Use functional components
function DashboardPage() {
  const { dashboardData } = useStore();
  
  useEffect(() => {
    // Component logic
  }, []);
  
  return <div>{/* JSX */}</div>;
}

// Use meaningful component names
// Prop validation with PropTypes or TypeScript
// Clear naming conventions
```

### Testing

#### Backend Tests

```python
# tests/test_recipes.py
import unittest
from app import create_app, db

class TestRecipes(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
    
    def test_generate_recipe(self):
        response = self.client.post('/api/recipes/generate', 
            json={'user_id': 1, 'cake_type': 'Chocolate'})
        self.assertEqual(response.status_code, 201)
```

#### Frontend Tests

```javascript
// tests/DashboardPage.test.jsx
import { render, screen } from '@testing-library/react';
import DashboardPage from '../pages/DashboardPage';

test('renders dashboard', () => {
  render(<DashboardPage />);
  expect(screen.getByText(/Total Orders/i)).toBeInTheDocument();
});
```

---

## Performance Optimization

### Backend Optimization

1. **Database:**
   - Use indexes
   - Lazy load relationships
   - Pagination
   - Query optimization

2. **Caching:**
   - Redis for frequent queries
   - Cache expensive AI calls
   - Session caching

3. **Code:**
   - Async operations
   - Connection pooling
   - Compression

### Frontend Optimization

1. **Code Splitting:**
   ```javascript
   const Dashboard = lazy(() => import('./pages/DashboardPage'));
   ```

2. **Bundle Optimization:**
   - Tree shaking
   - Minification
   - Asset compression

3. **Runtime:**
   - Memoization
   - Lazy loading
   - Virtual scrolling for lists

---

## Security Implementation

### Authentication

```python
# Password hashing (implement in production)
from werkzeug.security import generate_password_hash, check_password_hash

password_hash = generate_password_hash(password)
is_valid = check_password_hash(password_hash, password)
```

### Authorization

```python
# Check user ownership
@require_json()
def get_user_recipes(user_id):
    if current_user.id != user_id:
        return api_response("Unauthorized", None, 403)
```

### Input Validation

```python
# Backend validation
validators.validate_email(email)
validators.validate_positive_number(price)
validators.validate_cake_weight(weight)

# Frontend validation
if (!email.includes('@')) {
  showError('Invalid email');
}
```

### CORS Protection

```python
CORS(app, resources={
    r"/api/*": {
        "origins": os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','),
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## Deployment Considerations

### Environment Variables

```bash
# .env structure
DEBUG=False
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
SECRET_KEY=secret
OPENAI_API_KEY=sk-...
CORS_ORIGINS=https://domain.com
```

### Database Migrations

```bash
# Using Alembic (recommended for production)
flask db init
flask db migrate -m "Add users table"
flask db upgrade
```

### Scalability

1. **Horizontal Scaling:**
   - Stateless backend
   - Shared database
   - Cache layer (Redis)

2. **Load Balancing:**
   - Nginx load balancer
   - Session affinity
   - Health checks

---

## Monitoring & Logging

### Backend Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.info('Recipe generated successfully')
logger.error('Failed to connect to AI service', exc_info=True)
```

### Frontend Error Tracking

```javascript
// Sentry integration
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "https://key@sentry.io/project",
  environment: process.env.NODE_ENV,
});
```

---

## Common Development Tasks

### Add New Route

1. Create handler in `routes/module.py`:
```python
@auth_bp.route('/new-endpoint', methods=['POST'])
@api_response()
def new_endpoint():
    return {"data": "value"}
```

2. Add API client method in `frontend/services/api.js`:
```javascript
const newAPI = {
  callEndpoint: async (data) => {
    return apiClient.post('/new-endpoint', data);
  }
};
```

3. Use in component:
```javascript
const result = await newAPI.callEndpoint(data);
```

### Add New Database Model

1. Add model in `models/database.py`
2. Create route handlers
3. Add migrations
4. Update API client

### Add New Feature Page

1. Create component in `pages/`
2. Add route in `App.jsx`
3. Add menu item in `Layout.jsx`
4. Add store state if needed

---

**This architecture is scalable, maintainable, and production-ready!**
