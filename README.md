# Smart Home Bakery Management Platform

## 🎂 Project Overview

The **Smart Home Bakery Management Platform** is an AI-powered full-stack application designed to help home bakers and mothers:

- ✅ Generate perfect cake recipes using AI
- ✅ Calculate exact ingredient costs
- ✅ Manage inventory efficiently
- ✅ Track orders and profits
- ✅ Analyze market pricing
- ✅ Get AI-powered business insights
- ✅ Grow their home bakery business professionally

## 🏗️ Project Structure

```
CAKE/
├── backend/                    # Python Flask Backend
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   ├── models/
│   │   └── database.py        # SQLAlchemy ORM models
│   ├── routes/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── recipes.py         # Recipe management
│   │   ├── ingredients.py     # Inventory management
│   │   ├── orders.py          # Order management
│   │   ├── dashboard.py       # Analytics and reports
│   │   ├── ai.py              # AI integration endpoints
│   │   ├── expenses.py        # Expense tracking
│   │   └── market_rates.py    # Market analysis
│   ├── services/
│   │   ├── ai_service.py      # AI services (OpenAI, Gemini)
│   │   ├── scraping_service.py # Web scraping for market rates
│   │   └── calculation_service.py # Cost calculations
│   ├── utils/
│   │   └── helpers.py         # Utility functions
│   └── database/
│       └── schema.sql         # Database schema
│
├── frontend/                   # React Frontend
│   ├── public/
│   │   └── index.html         # HTML entry point
│   ├── src/
│   │   ├── App.jsx            # Main App component
│   │   ├── App.css            # Global styles
│   │   ├── index.js           # React initialization
│   │   ├── index.css          # Tailwind imports
│   │   ├── components/
│   │   │   └── Layout.jsx     # Main layout component
│   │   ├── pages/             # Page components
│   │   ├── services/
│   │   │   ├── api.js         # API client
│   │   │   └── store.js       # Zustand store
│   │   └── styles/            # CSS modules
│   ├── package.json           # NPM dependencies
│   ├── .env.example           # Environment variables
│   └── vite.config.js         # Vite configuration
│
└── docs/                       # Documentation
    ├── SETUP.md              # Installation guide
    ├── API.md                # API documentation
    ├── DATABASE.md           # Database schema
    └── FEATURES.md           # Feature list
```

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Initialize database:**
   ```bash
   flask db upgrade
   # Or manually run schema.sql
   ```

6. **Run development server:**
   ```bash
   python app.py
   # Or: flask run
   ```

   Server runs on http://localhost:5000

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with backend URL
   ```

4. **Run development server:**
   ```bash
   npm run dev
   ```

   Frontend runs on http://localhost:3000

## 🔑 Environment Variables

### Backend (.env)

```
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///cake_bakery.db
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
CORS_ORIGINS=http://localhost:3000
SERVER_PORT=5000
```

### Frontend (.env)

```
VITE_API_BASE_URL=http://localhost:5000/api
```

## 🗄️ Database

The application uses **SQLite** for simplicity in development. For production, consider using PostgreSQL.

**Key Tables:**
- `users` - Home bakers
- `recipes` - Cake recipes (AI-generated)
- `ingredients` - Inventory management
- `orders` - Customer orders
- `expenses` - Business expenses
- `profit_reports` - Analytics data
- `bakery_market_rates` - Competitor pricing
- `decoration_references` - Design inspiration

See [DATABASE.md](docs/DATABASE.md) for complete schema.

## 🤖 AI Integration

### Supported AI Providers

1. **OpenAI**
   - GPT-3.5-turbo for recipe generation
   - DALL-E 3 for image generation

2. **Google Gemini**
   - Backup recipe generation
   - Alternative to OpenAI

### AI Features

- Recipe generation based on parameters
- Decoration recommendations
- Baking mistake diagnosis
- Profit margin optimization
- Cake suggestions based on available ingredients
- Cake design image generation

See [FEATURES.md](docs/FEATURES.md) for detailed feature list.

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile/{user_id}` - Get user profile
- `PUT /api/auth/profile/{user_id}` - Update profile

### Recipes
- `POST /api/recipes/generate` - Generate recipe with AI
- `GET /api/recipes/{user_id}` - Get user's recipes
- `GET /api/recipes/{recipe_id}` - Get recipe details
- `POST /api/recipes/{recipe_id}/rate` - Rate recipe

### Ingredients
- `GET /api/ingredients/{user_id}` - Get inventory
- `POST /api/ingredients` - Add ingredient
- `POST /api/ingredients/{id}/use` - Use ingredient
- `GET /api/ingredients/{user_id}/alerts` - Get low stock alerts

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders/{user_id}` - Get user's orders
- `POST /api/orders/{order_id}/estimate` - Estimate order cost
- `POST /api/orders/{order_id}/finalize` - Finalize order

### Dashboard
- `GET /api/dashboard/{user_id}/summary` - Get dashboard summary
- `GET /api/dashboard/{user_id}/daily-profit` - Daily profit data
- `GET /api/dashboard/{user_id}/recipe-performance` - Recipe analytics

### AI
- `POST /api/ai/recipe-generator` - Generate recipe
- `POST /api/ai/decoration-recommendations` - Get decoration ideas
- `POST /api/ai/diagnose-mistake` - AI diagnosis for issues
- `POST /api/ai/optimize-profit` - Profit recommendations
- `POST /api/ai/suggest-cakes` - Cake suggestions
- `POST /api/ai/generate-image` - Generate cake image

### Market Rates
- `POST /api/market-rates/scrape` - Scrape competitor prices
- `GET /api/market-rates/{user_id}` - Get market rates
- `POST /api/market-rates/analyze/{user_id}` - Analyze pricing

See [API.md](docs/API.md) for complete API documentation.

## 🎨 Frontend Features

- **Responsive Design** - Mobile-first, works on all devices
- **Dark Mode** - Light and dark theme support
- **Real-time Updates** - Live data synchronization
- **Beautiful UI** - Tailwind CSS with custom components
- **Interactive Charts** - Profit and sales analytics
- **Form Validation** - Client-side input validation
- **Error Handling** - User-friendly error messages
- **Loading States** - Smooth loading indicators

## 🔐 Security

- Input validation on both frontend and backend
- Password hashing (implement bcrypt in production)
- CORS protection
- Environment variable security
- SQL injection prevention via SQLAlchemy ORM
- Rate limiting (recommended for production)
- HTTPS enforcement (recommended for production)

## 📱 Tech Stack

### Backend
- **Framework:** Flask 2.3
- **Database:** SQLite (PostgreSQL for production)
- **ORM:** SQLAlchemy 2.0
- **AI:** OpenAI API, Google Gemini API
- **Web Scraping:** BeautifulSoup, Selenium
- **Server:** Gunicorn (production)

### Frontend
- **Framework:** React 18
- **Routing:** React Router v6
- **State Management:** Zustand
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **Charts:** Chart.js
- **UI Components:** Lucide Icons
- **Build Tool:** Vite

### Database
- **SQLite** - Development
- **PostgreSQL** - Production (recommended)

## 🧪 Testing

```bash
# Backend tests
pytest backend/

# Frontend tests
npm test
```

## 📦 Deployment

### Backend (Heroku, AWS, DigitalOcean)

```bash
# Build
pip install -r requirements.txt

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend (Vercel, Netlify, AWS S3)

```bash
# Build
npm run build

# Deploy dist folder
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Email: support@smartbakery.local

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] SMS notifications
- [ ] Email delivery integration
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Voice commands
- [ ] Offline support
- [ ] Advanced AI features

## ✨ Features Implemented

### Core Features
- ✅ AI Recipe Generation
- ✅ Ingredient Cost Calculator
- ✅ Inventory Management
- ✅ Order Management
- ✅ Profit Analytics
- ✅ Market Price Analysis
- ✅ Decoration Recommendations
- ✅ Baking Mistake Diagnosis
- ✅ User Dashboard
- ✅ Expense Tracking

### AI Features
- ✅ OpenAI Integration
- ✅ Google Gemini Integration
- ✅ Recipe Generation
- ✅ Image Generation
- ✅ Profit Optimization
- ✅ Problem Diagnosis

### UI/UX
- ✅ Responsive Design
- ✅ Dark Mode
- ✅ Beautiful Dashboard
- ✅ Interactive Charts
- ✅ Real-time Updates

---

**Happy Baking! 🍰**
