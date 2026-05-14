# Quick Reference Guide

## Common Commands

### Backend (Python)

```bash
# Setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python app.py

# Test
pytest
pytest tests/test_recipes.py

# Code quality
black .
flake8

# Database
flask db init
flask db migrate -m "message"
flask db upgrade
```

### Frontend (React)

```bash
# Setup
cd frontend
npm install

# Development
npm run dev

# Build
npm run build

# Preview
npm run preview

# Test
npm test

# Lint
npm run lint

# Format
npm run format
```

## API Endpoints Quick Reference

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `GET /api/auth/profile/{id}` - Get profile

### Recipes
- `POST /api/recipes/generate` - Generate recipe
- `GET /api/recipes/{user_id}` - List recipes
- `GET /api/recipes/{id}` - Get recipe

### Ingredients
- `GET /api/ingredients/{user_id}` - List inventory
- `POST /api/ingredients` - Add ingredient
- `POST /api/ingredients/{id}/use` - Use ingredient

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders/{user_id}` - List orders
- `POST /api/orders/{id}/finalize` - Finalize order

### Dashboard
- `GET /api/dashboard/{user_id}/summary` - Summary
- `POST /api/dashboard/{user_id}/generate-report` - Generate report

### AI
- `POST /api/ai/recipe-generator` - Generate recipe
- `POST /api/ai/decoration-recommendations` - Decorations
- `POST /api/ai/generate-image` - Generate image

## Environment Variables

### Backend (.env)
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///cake_bakery.db
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:5000/api
```

## Database Quick Reference

### Key Tables
- `users` - Home bakers
- `recipes` - Cake recipes
- `ingredients` - Inventory
- `orders` - Customer orders
- `expenses` - Business expenses
- `profit_reports` - Analytics

### Common Queries

```sql
-- Total revenue per user (last 30 days)
SELECT 
  user_id, 
  SUM(selling_price) as revenue
FROM orders
WHERE order_date >= date('now', '-30 days')
GROUP BY user_id;

-- Most used ingredients
SELECT 
  i.name, 
  SUM(oi.quantity_used) as total_used
FROM ingredients i
JOIN order_items oi ON i.id = oi.ingredient_id
GROUP BY i.id
ORDER BY total_used DESC
LIMIT 10;

-- Low stock alerts
SELECT 
  name, 
  stock_quantity, 
  min_stock_alert
FROM ingredients
WHERE stock_quantity < min_stock_alert;
```

## Code Snippets

### Backend - Add New Route

```python
# routes/new_module.py
from flask import Blueprint, request
from utils.helpers import api_response, validate_inputs

new_bp = Blueprint('new', __name__, url_prefix='/api/new')

@new_bp.route('/endpoint', methods=['POST'])
@api_response()
def new_endpoint():
    data = request.get_json()
    # Process data
    return {"result": "success"}
```

### Frontend - API Call

```javascript
// services/api.js
const newAPI = {
  fetchData: async (id) => {
    return apiClient.get(`/new/endpoint/${id}`);
  },
  postData: async (data) => {
    return apiClient.post('/new/endpoint', data);
  }
};
```

### Frontend - Component

```javascript
// pages/NewPage.jsx
import { useEffect, useState } from 'react';
import { newAPI } from '../services/api';

export default function NewPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const result = await newAPI.fetchData(1);
        setData(result);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  return <div>{JSON.stringify(data)}</div>;
}
```

## File Locations

| Item | Location |
|------|----------|
| Backend config | `backend/config.py` |
| Database models | `backend/models/database.py` |
| Routes | `backend/routes/` |
| Services | `backend/services/` |
| Frontend pages | `frontend/src/pages/` |
| Components | `frontend/src/components/` |
| Global store | `frontend/src/services/store.js` |
| API client | `frontend/src/services/api.js` |
| Styles | `frontend/src/App.css` |
| Tailwind config | `frontend/tailwind.config.js` |

## Useful Links

- [Flask Docs](https://flask.palletsprojects.com/)
- [React Docs](https://react.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Zustand](https://github.com/pmndrs/zustand)

## Debugging

### Backend
```bash
# Debug with Flask CLI
FLASK_ENV=development FLASK_DEBUG=1 flask run

# Check database
sqlite3 cake_bakery.db
.tables
.schema recipes
SELECT * FROM recipes;
```

### Frontend
```bash
# Check console (F12)
console.log('Debug:', variable);

# React DevTools
# Install browser extension

# Network tab
# Monitor API requests
```

## Port References

| Service | Port | URL |
|---------|------|-----|
| Backend | 5000 | http://localhost:5000 |
| Frontend | 3000 | http://localhost:3000 |
| API | 5000 | http://localhost:5000/api |

## Important Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `SETUP.md` | Installation guide |
| `API.md` | API documentation |
| `DATABASE.md` | Database schema |
| `ARCHITECTURE.md` | System design |
| `FEATURES.md` | Feature list |
| `TROUBLESHOOTING.md` | Common issues |
| `DEPLOYMENT.md` | Deployment guide |

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

## Git Quick Reference

```bash
# Clone
git clone <repo-url>

# Create branch
git checkout -b feature/name

# Add changes
git add .

# Commit
git commit -m "feat: description"

# Push
git push origin feature/name

# Update
git pull origin main

# Rebase
git rebase origin/main

# Reset
git reset --hard origin/main
```

## Regular Maintenance

### Weekly
- [ ] Check GitHub issues
- [ ] Review pull requests
- [ ] Update dependencies

### Monthly
- [ ] Database backup
- [ ] Security audit
- [ ] Performance review
- [ ] Dependency updates

## Performance Tips

- Backend: Use pagination, indexes, caching
- Frontend: Code splitting, lazy loading, compression
- Database: Query optimization, proper indexing
- API: Compression, response caching

## Security Reminders

✅ DO:
- Use environment variables for secrets
- Validate all user inputs
- Sanitize database queries
- Use HTTPS in production
- Regular backups

❌ DON'T:
- Hardcode secrets
- Trust user input
- Skip validation
- Expose error details
- Ignore security updates

---

**Keep this handy while developing! 📋**
