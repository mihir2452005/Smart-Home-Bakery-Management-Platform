"""
Ingredients Routes
Inventory management and ingredient tracking
"""

from flask import Blueprint, request
from models.database import db, Ingredient, InventoryAlert, RecipeIngredient
from utils.helpers import api_response, require_json, validate_inputs, Helpers, Validators

ingredients_bp = Blueprint('ingredients', __name__)


@ingredients_bp.route('/<int:user_id>', methods=['GET'])
def get_ingredients(user_id):
    """Get all ingredients for a user"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    
    query = Ingredient.query.filter_by(user_id=user_id)
    
    if category:
        query = query.filter_by(category=category)
    
    query = query.order_by(Ingredient.name)
    items, total_count, total_pages = Helpers.paginate_query(query, page)
    
    ingredients_data = [{
        "id": ing.id,
        "name": ing.name,
        "category": ing.category,
        "unit": ing.unit,
        "price_per_unit": ing.price_per_unit,
        "total_quantity": ing.total_quantity,
        "stock_quantity": ing.stock_quantity,
        "min_stock_alert": ing.min_stock_alert,
        "cost_per_unit": ing.price_per_unit,
        "total_cost": ing.price_per_unit * ing.total_quantity,
        "supplier": ing.supplier,
        "last_purchased_date": ing.last_purchased_date.isoformat() if ing.last_purchased_date else None
    } for ing in items]
    
    pagination_data = Helpers.generate_pagination_data(
        ingredients_data, total_count, total_pages, page
    )
    
    return api_response(
        status="success",
        data=pagination_data
    )


@ingredients_bp.route('/', methods=['POST'])
@require_json
@validate_inputs(['user_id', 'name', 'category', 'unit', 'price_per_unit', 'total_quantity'])
def add_ingredient():
    """Add new ingredient to inventory"""
    data = request.get_json()
    
    if not Validators.validate_positive_number(data['price_per_unit']):
        return api_response(
            status="error",
            message="Price per unit must be positive",
            code=400
        )
    
    if not Validators.validate_positive_number(data['total_quantity']):
        return api_response(
            status="error",
            message="Total quantity must be positive",
            code=400
        )
    
    try:
        ingredient = Ingredient(
            user_id=data['user_id'],
            name=data['name'],
            category=data['category'],
            unit=data['unit'],
            price_per_unit=data['price_per_unit'],
            total_quantity=data['total_quantity'],
            stock_quantity=data['total_quantity'],
            min_stock_alert=data.get('min_stock_alert'),
            supplier=data.get('supplier'),
            last_purchased_date=data.get('last_purchased_date')
        )
        
        db.session.add(ingredient)
        db.session.commit()
        
        return api_response(
            status="success",
            message="Ingredient added successfully!",
            data={
                "id": ingredient.id,
                "name": ingredient.name,
                "category": ingredient.category,
                "stock_quantity": ingredient.stock_quantity
            },
            code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Failed to add ingredient: {str(e)}",
            code=500
        )


@ingredients_bp.route('/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    """Get ingredient details"""
    ingredient = Ingredient.query.get(ingredient_id)
    
    if not ingredient:
        return api_response(
            status="error",
            message="Ingredient not found",
            code=404
        )
    
    return api_response(
        status="success",
        data={
            "id": ingredient.id,
            "name": ingredient.name,
            "category": ingredient.category,
            "unit": ingredient.unit,
            "price_per_unit": ingredient.price_per_unit,
            "total_quantity": ingredient.total_quantity,
            "stock_quantity": ingredient.stock_quantity,
            "min_stock_alert": ingredient.min_stock_alert,
            "total_cost": ingredient.price_per_unit * ingredient.total_quantity,
            "supplier": ingredient.supplier,
            "last_purchased_date": ingredient.last_purchased_date.isoformat() if ingredient.last_purchased_date else None
        }
    )


@ingredients_bp.route('/<int:ingredient_id>', methods=['PUT'])
@require_json
def update_ingredient(ingredient_id):
    """Update ingredient"""
    ingredient = Ingredient.query.get(ingredient_id)
    
    if not ingredient:
        return api_response(
            status="error",
            message="Ingredient not found",
            code=404
        )
    
    data = request.get_json()
    
    # Update allowed fields
    if 'name' in data:
        ingredient.name = data['name']
    if 'price_per_unit' in data:
        if not Validators.validate_positive_number(data['price_per_unit']):
            return api_response(
                status="error",
                message="Price per unit must be positive",
                code=400
            )
        ingredient.price_per_unit = data['price_per_unit']
    if 'total_quantity' in data:
        ingredient.total_quantity = data['total_quantity']
    if 'stock_quantity' in data:
        ingredient.stock_quantity = data['stock_quantity']
    if 'min_stock_alert' in data:
        ingredient.min_stock_alert = data['min_stock_alert']
    if 'supplier' in data:
        ingredient.supplier = data['supplier']
    
    try:
        db.session.commit()
        return api_response(
            status="success",
            message="Ingredient updated!",
            data={"id": ingredient.id, "name": ingredient.name}
        )
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Update failed: {str(e)}",
            code=500
        )


@ingredients_bp.route('/<int:ingredient_id>/use', methods=['POST'])
@require_json
@validate_inputs(['quantity_used'])
def use_ingredient(ingredient_id):
    """Use/consume ingredient from stock"""
    ingredient = Ingredient.query.get(ingredient_id)
    
    if not ingredient:
        return api_response(
            status="error",
            message="Ingredient not found",
            code=404
        )
    
    data = request.get_json()
    quantity_used = data['quantity_used']
    
    if quantity_used > ingredient.stock_quantity:
        return api_response(
            status="error",
            message=f"Insufficient stock. Available: {ingredient.stock_quantity}",
            code=400
        )
    
    try:
        ingredient.stock_quantity -= quantity_used
        cost_used = ingredient.get_cost_used(quantity_used)
        
        # Check if stock is low
        if ingredient.min_stock_alert and ingredient.stock_quantity <= ingredient.min_stock_alert:
            # Create alert
            alert = InventoryAlert(
                user_id=ingredient.user_id,
                ingredient_id=ingredient_id,
                alert_type='low_stock',
                message=f"{ingredient.name} stock is running low!"
            )
            db.session.add(alert)
        
        db.session.commit()
        
        return api_response(
            status="success",
            message="Ingredient consumed!",
            data={
                "ingredient_id": ingredient_id,
                "quantity_used": quantity_used,
                "cost_used": round(cost_used, 2),
                "stock_remaining": ingredient.stock_quantity
            }
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Failed to update: {str(e)}",
            code=500
        )


@ingredients_bp.route('/<int:user_id>/alerts', methods=['GET'])
def get_inventory_alerts(user_id):
    """Get inventory alerts for user"""
    alerts = InventoryAlert.query.filter_by(
        user_id=user_id,
        is_resolved=False
    ).all()
    
    alerts_data = [{
        "id": alert.id,
        "ingredient_id": alert.ingredient_id,
        "ingredient_name": alert.ingredient.name,
        "alert_type": alert.alert_type,
        "message": alert.message,
        "created_at": alert.created_at.isoformat()
    } for alert in alerts]
    
    return api_response(
        status="success",
        data=alerts_data
    )


@ingredients_bp.route('/alerts/<int:alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    """Resolve inventory alert"""
    from datetime import datetime
    
    alert = InventoryAlert.query.get(alert_id)
    
    if not alert:
        return api_response(
            status="error",
            message="Alert not found",
            code=404
        )
    
    try:
        alert.is_resolved = True
        alert.resolved_at = datetime.utcnow()
        db.session.commit()
        
        return api_response(
            status="success",
            message="Alert resolved!"
        )
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Failed: {str(e)}",
            code=500
        )


@ingredients_bp.route('/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    """Delete ingredient"""
    ingredient = Ingredient.query.get(ingredient_id)
    
    if not ingredient:
        return api_response(
            status="error",
            message="Ingredient not found",
            code=404
        )
    
    try:
        db.session.delete(ingredient)
        db.session.commit()
        
        return api_response(
            status="success",
            message="Ingredient deleted!"
        )
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Delete failed: {str(e)}",
            code=500
        )
