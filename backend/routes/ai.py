"""
AI Routes
AI-powered features and recommendations
"""

from flask import Blueprint, request, current_app
from models.database import db, AIGeneratedImage, DecorationReference
from services.ai_service import AIService, CalculationService
from services.scraping_service import ScrapingService
from utils.helpers import api_response, require_json, validate_inputs

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/recipe-generator', methods=['POST'])
@require_json
@validate_inputs(['cake_weight', 'flavor', 'budget', 'oven_type', 'servings'])
def generate_recipe():
    """
    Generate AI-powered recipe
    Delegates to recipe generation endpoint
    """
    from routes.recipes import generate_recipe as recipe_generator
    return recipe_generator()


@ai_bp.route('/decoration-recommendations', methods=['POST'])
@require_json
@validate_inputs(['cake_weight', 'style'])
def get_decoration_recommendations():
    """
    Get AI decoration recommendations
    
    Required fields:
    - cake_weight: '500g', '1kg', '2kg', '3kg'
    - style: Decoration style
    """
    data = request.get_json()
    
    try:
        ai_service = AIService()
        result = ai_service.generate_decoration_recommendations(
            cake_weight=data['cake_weight'],
            base_style=data['style']
        )
        
        if not result.get('success'):
            return api_response(
                status="error",
                message="Failed to generate recommendations",
                code=500
            )
        
        # Store reference if user ID provided
        if 'user_id' in data:
            reference = DecorationReference(
                user_id=data['user_id'],
                cake_weight=data['cake_weight'],
                style=data['style'],
                cream_quantity_grams=result['data'].get('cream_quantity_grams'),
                piping_style=result['data'].get('piping_style'),
                drip_design=result['data'].get('drip_design'),
                flower_quantity=result['data'].get('flower_quantity'),
                fondant_usage=result['data'].get('fondant_usage'),
                difficulty_level=result['data'].get('difficulty_level'),
                estimated_time_hours=result['data'].get('estimated_time_hours'),
                description=result['data'].get('style_name')
            )
            db.session.add(reference)
            db.session.commit()
        
        return api_response(
            status="success",
            data=result['data']
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Error generating recommendations: {str(e)}",
            code=500
        )


@ai_bp.route('/diagnose-mistake', methods=['POST'])
@require_json
@validate_inputs(['problem_description', 'cake_type'])
def diagnose_baking_mistake():
    """
    AI diagnosis for baking problems
    
    Required fields:
    - problem_description: Description of the problem
    - cake_type: Type of cake
    """
    data = request.get_json()
    
    try:
        ai_service = AIService()
        result = ai_service.diagnose_baking_mistake(
            problem_description=data['problem_description'],
            cake_type=data['cake_type']
        )
        
        if not result.get('success'):
            return api_response(
                status="error",
                message="Failed to diagnose",
                code=500
            )
        
        return api_response(
            status="success",
            data=result['data']
        )
    
    except Exception as e:
        return api_response(
            status="error",
            message=f"Diagnosis failed: {str(e)}",
            code=500
        )


@ai_bp.route('/optimize-profit', methods=['POST'])
@require_json
@validate_inputs(['ingredient_costs', 'selling_price', 'cake_type', 'market_rate'])
def optimize_profit():
    """
    AI profit optimization
    
    Required fields:
    - ingredient_costs: Total ingredient cost
    - selling_price: Current selling price
    - cake_type: Type of cake
    - market_rate: Market average rate
    """
    data = request.get_json()
    
    try:
        ai_service = AIService()
        result = ai_service.optimize_profit_margin(
            ingredient_costs=data['ingredient_costs'],
            selling_price=data['selling_price'],
            cake_type=data['cake_type'],
            market_rate=data['market_rate']
        )
        
        if not result.get('success'):
            return api_response(
                status="error",
                message="Failed to optimize",
                code=500
            )
        
        return api_response(
            status="success",
            data=result['data']
        )
    
    except Exception as e:
        return api_response(
            status="error",
            message=f"Optimization failed: {str(e)}",
            code=500
        )


@ai_bp.route('/suggest-cakes', methods=['POST'])
@require_json
@validate_inputs(['available_ingredients', 'budget'])
def suggest_cakes():
    """
    Suggest cakes based on available ingredients
    
    Required fields:
    - available_ingredients: List of available ingredients
    - budget: Budget in INR
    """
    data = request.get_json()
    
    try:
        ai_service = AIService()
        result = ai_service.suggest_cakes_from_ingredients(
            available_ingredients=data['available_ingredients'],
            budget=data['budget']
        )
        
        if not result.get('success'):
            return api_response(
                status="error",
                message="Failed to generate suggestions",
                code=500
            )
        
        return api_response(
            status="success",
            data=result['data']
        )
    
    except Exception as e:
        return api_response(
            status="error",
            message=f"Suggestion failed: {str(e)}",
            code=500
        )


@ai_bp.route('/generate-image', methods=['POST'])
@require_json
@validate_inputs(['user_id', 'cake_description'])
def generate_cake_image():
    """
    Generate AI cake design preview
    
    Required fields:
    - user_id: User ID
    - cake_description: Cake design description
    """
    data = request.get_json()
    
    try:
        ai_service = AIService()
        result = ai_service.generate_cake_image(cake_description=data['cake_description'])
        
        if not result.get('success'):
            return api_response(
                status="error",
                message="Failed to generate image",
                code=500
            )
        
        # Store image record
        ai_image = AIGeneratedImage(
            user_id=data['user_id'],
            prompt=data['cake_description'],
            image_url=result['image_url'],
            ai_provider=result.get('ai_provider', 'openai'),
            model_used='dall-e-3'
        )
        
        db.session.add(ai_image)
        db.session.commit()
        
        return api_response(
            status="success",
            message="Image generated successfully!",
            data={
                "image_id": ai_image.id,
                "image_url": result['image_url'],
                "ai_provider": result.get('ai_provider')
            },
            code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Image generation failed: {str(e)}",
            code=500
        )


@ai_bp.route('/calculate-cost', methods=['POST'])
@require_json
@validate_inputs(['used_quantity', 'total_quantity', 'total_price'])
def calculate_ingredient_cost():
    """
    Calculate ingredient cost using formula
    
    Formula: (Used Quantity / Total Quantity) × Total Price
    """
    data = request.get_json()
    
    cost = CalculationService.calculate_ingredient_cost(
        used_quantity=data['used_quantity'],
        total_quantity=data['total_quantity'],
        total_price=data['total_price']
    )
    
    return api_response(
        status="success",
        data={
            "used_quantity": data['used_quantity'],
            "cost": round(cost, 2)
        }
    )


@ai_bp.route('/suggest-price', methods=['POST'])
@require_json
@validate_inputs(['total_cost', 'market_rate'])
def suggest_selling_price():
    """
    Suggest selling price for cake
    
    Required fields:
    - total_cost: Total ingredient cost
    - market_rate: Market average price
    - desired_margin: Desired profit margin (optional, default 40%)
    """
    data = request.get_json()
    
    suggested_price = CalculationService.suggest_selling_price(
        total_cost=data['total_cost'],
        market_rate=data['market_rate'],
        desired_margin=data.get('desired_margin', 40)
    )
    
    profit_margin = ((suggested_price - data['total_cost']) / suggested_price) * 100
    
    return api_response(
        status="success",
        data={
            "suggested_price": round(suggested_price, 2),
            "cost": data['total_cost'],
            "profit": round(suggested_price - data['total_cost'], 2),
            "profit_margin": round(profit_margin, 2)
        }
    )


@ai_bp.route('/<int:user_id>/generated-images', methods=['GET'])
def get_generated_images(user_id):
    """Get all generated images for user"""
    images = AIGeneratedImage.query.filter_by(user_id=user_id).order_by(
        AIGeneratedImage.created_at.desc()
    ).all()
    
    images_data = [{
        "id": img.id,
        "prompt": img.prompt,
        "image_url": img.image_url,
        "ai_provider": img.ai_provider,
        "created_at": img.created_at.isoformat()
    } for img in images]
    
    return api_response(
        status="success",
        data=images_data
    )
