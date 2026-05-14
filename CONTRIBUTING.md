# Contributing Guide

## Welcome to Smart Home Bakery Platform! 🎂

Thank you for interest in contributing! This guide will help you get started.

## Getting Started

### 1. Fork and Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/your-username/cake-bakery.git
cd cake-bakery

# Add upstream for sync
git remote add upstream https://github.com/original-owner/cake-bakery.git
```

### 2. Set Up Development Environment

Follow the setup guide in [SETUP.md](SETUP.md):

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
# or
git checkout -b docs/documentation-update
```

### 2. Make Changes

Follow coding standards:

**Backend (Python):**
- Follow PEP 8
- Use type hints
- Add docstrings
- 4 spaces indentation
- Keep functions focused and small

**Frontend (JavaScript/React):**
- Use functional components
- Follow ESLint rules
- Use meaningful variable names
- Add comments for complex logic
- Use const/let, not var

### 3. Test Your Changes

**Backend:**
```bash
# Run tests
pytest tests/

# Check code quality
black .
flake8

# Run specific test
pytest tests/test_recipes.py::TestRecipes::test_generate_recipe
```

**Frontend:**
```bash
# Run tests
npm test

# Run specific test
npm test -- DashboardPage.test

# Build check
npm run build
```

### 4. Commit Changes

Use conventional commits:

```bash
git add .

# Good commit messages:
git commit -m "feat: add recipe rating feature"
git commit -m "fix: resolve pagination issue in orders"
git commit -m "docs: add API documentation"
git commit -m "refactor: simplify profit calculation"
git commit -m "test: add tests for ingredient validation"

# Avoid:
# "bug fix" ❌
# "updated stuff" ❌
# "asdf" ❌
```

### 5. Keep Branch Up to Date

```bash
git fetch upstream
git rebase upstream/main

# If conflicts occur, resolve them:
# 1. Fix conflicted files
git add resolved_file.py
git rebase --continue
```

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name

# Create PR on GitHub with:
# - Clear title
# - Description of changes
# - Related issues (Fixes #123)
# - Testing notes
```

## Pull Request Process

### PR Title Format
- `feat: Add recipe rating system`
- `fix: Resolve database connection leak`
- `docs: Update API documentation`

### PR Checklist

Before submitting PR:

- [ ] Code follows project style
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Changes are focused (not too many changes in one PR)
- [ ] Committed with meaningful messages
- [ ] Branch is up to date with main

### Code Review

Reviewers will check:
1. Code quality and style
2. Test coverage
3. Documentation
4. Potential issues
5. Performance impact

## Types of Contributions

### 🐛 Bug Fixes

1. Create issue describing the bug
2. Create branch: `fix/bug-description`
3. Fix the bug
4. Add test that would catch this bug
5. Document the fix in PR

### ✨ New Features

1. Discuss feature in an issue first
2. Create branch: `feature/feature-name`
3. Implement feature
4. Add comprehensive tests
5. Update documentation
6. Update FEATURES.md

### 📚 Documentation

1. Check for clarity and accuracy
2. Fix typos and improve explanations
3. Add missing information
4. Create branch: `docs/description`
5. Submit PR

### 🎨 UI/UX Improvements

1. Create issue with screenshots
2. Implement improvement
3. Test on multiple devices
4. Include before/after screenshots
5. Add accessibility notes

## Project Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed structure.

Quick overview:
```
backend/           Python Flask backend
├── routes/       API endpoints
├── services/     Business logic
├── models/       Database models
└── utils/        Helper functions

frontend/         React frontend
├── pages/        Page components
├── components/   Reusable components
├── services/     API client & store
└── styles/       CSS styling
```

## Coding Standards

### Backend (Python)

```python
# Good example
def calculate_profit_margin(revenue: float, cost: float) -> float:
    """Calculate profit margin percentage.
    
    Args:
        revenue: Total revenue amount
        cost: Total cost amount
        
    Returns:
        Profit margin as percentage (0-100)
    """
    if cost == 0:
        return 0
    return ((revenue - cost) / revenue) * 100


# Bad example
def calc(r,c):
    return ((r - c) / r) * 100
```

### Frontend (JavaScript/React)

```javascript
// Good example
function RecipeCard({ recipe, onSelect }) {
  const handleClick = () => {
    onSelect(recipe.id);
  };

  return (
    <div className="recipe-card">
      <h3>{recipe.name}</h3>
      <button onClick={handleClick}>View Details</button>
    </div>
  );
}

// Bad example
function rc({ r, o }) {
  return <div><h3>{r.n}</h3><button onClick={() => o(r.id)}>Click</button></div>;
}
```

## Testing

### Backend Tests

```python
# tests/test_recipes.py
import unittest
from app import create_app, db

class TestRecipeGeneration(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_generate_chocolate_cake(self):
        response = self.client.post('/api/recipes/generate', json={
            'user_id': 1,
            'cake_type': 'Chocolate',
            'weight': '1kg'
        })
        self.assertEqual(response.status_code, 201)
```

### Frontend Tests

```javascript
// pages/RecipeGenerator.test.jsx
import { render, screen, userEvent } from '@testing-library/react';
import RecipeGenerator from './RecipeGenerator';

test('generates recipe with user input', async () => {
  render(<RecipeGenerator />);
  
  const generateBtn = screen.getByRole('button', { name: /generate/i });
  await userEvent.click(generateBtn);
  
  expect(screen.getByText(/recipe generated/i)).toBeInTheDocument();
});
```

## Issue Guidelines

### When Creating an Issue

1. **Check existing issues** first
2. **Use clear title** - describe the problem
3. **Provide context:**
   - What were you trying to do?
   - What happened?
   - What did you expect?
4. **Include details:**
   - Steps to reproduce
   - Screenshots/videos if applicable
   - Error messages (full text)
   - System information
5. **Label appropriately:**
   - `bug` - Something broken
   - `enhancement` - New feature
   - `documentation` - Doc improvement
   - `question` - Need clarification

### Issue Template

```markdown
## Description
Brief description of the issue

## Steps to Reproduce
1. Go to...
2. Click on...
3. See error...

## Expected Behavior
What should happen?

## Actual Behavior
What actually happened?

## Environment
- Python version: 3.10
- Node version: 16
- OS: Windows/Mac/Linux

## Screenshots
[If applicable]

## Additional Context
[Any other information]
```

## Code Review Guidelines

### For Contributors

Be open to feedback:
- Respond to comments constructively
- Make requested changes
- Ask for clarification if needed
- Thank reviewers

### For Reviewers

Be supportive:
- Praise good work
- Explain why changes are needed
- Suggest improvements
- Be respectful and helpful

## Performance Guidelines

### Backend
- Avoid N+1 queries (use eager loading)
- Use pagination for large datasets
- Cache expensive operations
- Index frequently queried columns

### Frontend
- Use code splitting for routes
- Lazy load heavy components
- Memoize expensive computations
- Monitor bundle size

## Security Guidelines

- Never commit secrets (API keys, passwords)
- Use environment variables
- Validate all user inputs
- Sanitize database queries (use ORM)
- Enable HTTPS in production
- Keep dependencies updated

## Documentation

All significant changes need documentation:

1. **Code comments** for complex logic
2. **Docstrings** for functions/classes
3. **README updates** if changing setup
4. **API documentation** for new endpoints
5. **FEATURES.md** for new features

## Branches

| Type | Naming | Example |
|------|--------|---------|
| Feature | `feature/` | `feature/recipe-rating` |
| Bug Fix | `fix/` | `fix/pagination-error` |
| Documentation | `docs/` | `docs/api-guide` |
| Refactor | `refactor/` | `refactor/store-logic` |
| Test | `test/` | `test/recipe-generation` |

## Commit Message Guidelines

Format: `<type>(<scope>): <subject>`

```
feat(recipes): add cake weight parameter
fix(orders): resolve profit calculation error
docs(setup): clarify database setup steps
style(frontend): format CSS classes
refactor(backend): simplify profit logic
test(ingredients): add inventory tests
```

## Getting Help

- **Questions?** Create a discussion
- **Bug?** File an issue
- **Idea?** Start a discussion
- **Stuck?** Ask in issue comments

## Communication

- Be respectful and inclusive
- Provide constructive feedback
- Assume good intent
- Ask questions when unclear

## Recognition

Contributors are recognized in:
1. Commit history
2. GitHub contributors page
3. Release notes
4. Project README (for major contributions)

## Code of Conduct

- Be inclusive and welcoming
- Be respectful of differing opinions
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy to others

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to make Smart Home Bakery Platform better! 🎉**

Need help? Create an issue or reach out to maintainers.
