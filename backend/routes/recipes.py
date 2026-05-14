"""
Recipes Routes
Recipe management and generation
"""

from flask import Blueprint, request
from models.database import db, Recipe, RecipeInstruction, RecipeIngredient, Ingredient
from services.ai_service import AIService
from utils.helpers import api_response, require_json, validate_inputs, Helpers

recipes_bp = Blueprint('recipes', __name__)


@recipes_bp.route('/generate', methods=['POST'])
@require_json
@validate_inputs(['user_id', 'cake_weight', 'flavor', 'budget', 'oven_type', 'servings'])
def generate_recipe():
    """
    Generate AI-powered cake recipe
    
    Required fields:
    - user_id: User ID
    - cake_weight: '500g', '1kg', '2kg', '3kg'
    - flavor: Cake flavor
    - budget: Budget in INR
    - oven_type: 'microwave', 'gas_oven', 'electric_oven'
    - servings: Number of servings
    - is_eggless: Boolean (optional)
    """
    data = request.get_json()
    
    # Validate cake weight
    if data['cake_weight'] not in ['500g', '1kg', '2kg', '3kg']:
        return api_response(
            status="error",
            message="Invalid cake weight. Use: 500g, 1kg, 2kg, 3kg",
            code=400
        )
    
    try:
        # Generate recipe using AI
        ai_service = AIService()
        result = ai_service.generate_recipe(
            cake_weight=data['cake_weight'],
            flavor=data['flavor'],
            budget=data['budget'],
            oven_type=data['oven_type'],
            servings=data['servings'],
            is_eggless=data.get('is_eggless', False)
        )
        
        if not result.get('success'):
            return api_response(
                status="error",
                message="Failed to generate recipe",
                code=500
            )
        
        recipe_data = result['data']
        
        # Create recipe in database
        recipe = Recipe(
            user_id=data['user_id'],
            name=recipe_data.get('name', f"{data['flavor']} Cake"),
            cake_type=data['flavor'],
            weight=data['cake_weight'],
            servings=data.get('servings'),
            is_eggless=data.get('is_eggless', False),
            baking_temp=recipe_data.get('baking_temp'),
            baking_time=recipe_data.get('baking_time'),
            tin_size=recipe_data.get('tin_size'),
            difficulty_level=recipe_data.get('difficulty_level', 'medium'),
            ai_generated=True
        )
        
        db.session.add(recipe)
        db.session.flush()  # Get recipe ID
        
        # Add instructions
        for idx, instruction in enumerate(recipe_data.get('instructions', []), 1):
            rec_instruction = RecipeInstruction(
                recipe_id=recipe.id,
                step_number=instruction.get('step', idx),
                instruction=instruction.get('instruction'),
                duration_minutes=instruction.get('duration_minutes')
            )
            db.session.add(rec_instruction)
        
        db.session.commit()
        
        return api_response(
            status="success",
            message="Recipe generated successfully!",
            data={
                "recipe_id": recipe.id,
                "name": recipe.name,
                "cake_type": recipe.cake_type,
                "weight": recipe.weight,
                "baking_temp": recipe.baking_temp,
                "baking_time": recipe.baking_time,
                "ingredients": recipe_data.get('ingredients'),
                "instructions": recipe_data.get('instructions'),
                "difficulty_level": recipe.difficulty_level,
                "estimated_cost": recipe_data.get('estimated_cost')
            },
            code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Error generating recipe: {str(e)}",
            code=500
        )


@recipes_bp.route('/<int:user_id>', methods=['GET'])
def get_recipes(user_id):
    """Get all recipes for a user"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Recipe.query.filter_by(user_id=user_id).order_by(Recipe.created_at.desc())
    items, total_count, total_pages = Helpers.paginate_query(query, page, per_page)
    
    recipes_data = [{
        "id": recipe.id,
        "name": recipe.name,
        "cake_type": recipe.cake_type,
        "weight": recipe.weight,
        "servings": recipe.servings,
        "baking_time": recipe.baking_time,
        "difficulty_level": recipe.difficulty_level,
        "times_made": recipe.times_made,
        "rating": recipe.rating,
        "created_at": recipe.created_at.isoformat()
    } for recipe in items]
    
    pagination_data = Helpers.generate_pagination_data(
        recipes_data, total_count, total_pages, page, per_page
    )
    
    return api_response(
        status="success",
        data=pagination_data
    )


@recipes_bp.route('/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """Get specific recipe details"""
    recipe = Recipe.query.get(recipe_id)
    
    if not recipe:
        return api_response(
            status="error",
            message="Recipe not found",
            code=404
        )
    
    # Get ingredients
    ingredients = []
    for rec_ing in recipe.ingredients:
        ingredients.append({
            "id": rec_ing.ingredient_id,
            "name": rec_ing.ingredient.name,
            "quantity": rec_ing.quantity,
            "unit": rec_ing.unit,
            "is_optional": rec_ing.is_optional
        })
    
    # Get instructions
    instructions = [{
        "step": inst.step_number,
        "instruction": inst.instruction,
        "duration_minutes": inst.duration_minutes
    } for inst in recipe.instructions]
    
    return api_response(
        status="success",
        data={
            "id": recipe.id,
            "name": recipe.name,
            "cake_type": recipe.cake_type,
            "weight": recipe.weight,
            "servings": recipe.servings,
            "is_eggless": recipe.is_eggless,
            "baking_temp": recipe.baking_temp,
            "baking_time": recipe.baking_time,
            "tin_size": recipe.tin_size,
            "difficulty_level": recipe.difficulty_level,
            "ingredients": ingredients,
            "instructions": instructions,
            "times_made": recipe.times_made,
            "rating": recipe.rating,
            "created_at": recipe.created_at.isoformat()
        }
    )


@recipes_bp.route('/<int:recipe_id>/rate', methods=['POST'])
@require_json
def rate_recipe(recipe_id):
    """Rate recipe and update times made"""
    recipe = Recipe.query.get(recipe_id)
    
    if not recipe:
        return api_response(
            status="error",
            message="Recipe not found",
            code=404
        )
    
    data = request.get_json()
    
    if 'rating' in data:
        rating = data['rating']
        if 0 <= rating <= 5:
            # Update average rating
            if recipe.rating == 0:
                recipe.rating = rating
            else:
                recipe.rating = (recipe.rating + rating) / 2
    
    if 'times_made' in data:
        recipe.times_made += 1
    
    try:
        db.session.commit()
        return api_response(
            status="success",
            message="Recipe updated!",
            data={
                "rating": recipe.rating,
                "times_made": recipe.times_made
            }
        )
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Update failed: {str(e)}",
            code=500
        )


@recipes_bp.route('/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """Delete recipe"""
    recipe = Recipe.query.get(recipe_id)
    
    if not recipe:
        return api_response(
            status="error",
            message="Recipe not found",
            code=404
        )
    
    try:
        db.session.delete(recipe)
        db.session.commit()
        
        return api_response(
            status="success",
            message="Recipe deleted successfully!"
        )
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Delete failed: {str(e)}",
            code=500
        )


@recipes_bp.route('/search', methods=['GET'])
def search_recipes():
    """Search recipes by cake type"""
    cake_type = request.args.get('cake_type', '')
    user_id = request.args.get('user_id', type=int)
    
    query = Recipe.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    if cake_type:
        query = query.filter(Recipe.cake_type.ilike(f'%{cake_type}%'))
    
    recipes = query.all()
    
    recipes_data = [{
        "id": recipe.id,
        "name": recipe.name,
        "cake_type": recipe.cake_type,
        "weight": recipe.weight,
        "difficulty_level": recipe.difficulty_level
    } for recipe in recipes]
    
    return api_response(
        status="success",
        data=recipes_data
    )
