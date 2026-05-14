"""
Orders Routes
Order management and tracking
"""

from flask import Blueprint, request
from datetime import datetime, date
from models.database import db, Order, OrderItem, Ingredient
from services.ai_service import CalculationService, AIService
from utils.helpers import api_response, require_json, validate_inputs, Helpers

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/', methods=['POST'])
@require_json
@validate_inputs(['user_id', 'customer_name', 'cake_type', 'order_date', 'delivery_date'])
def create_order():
    """
    Create new order
    
    Required fields:
    - user_id: User ID
    - customer_name: Customer name
    - cake_type: Type of cake
    - order_date: Date order was placed
    - delivery_date: Date of delivery
    """
    data = request.get_json()
    
    try:
        order = Order(
            user_id=data['user_id'],
            customer_name=data['customer_name'],
            customer_phone=data.get('customer_phone'),
            customer_email=data.get('customer_email'),
            cake_type=data['cake_type'],
            cake_weight=data.get('cake_weight'),
            flavor=data.get('flavor'),
            theme=data.get('theme'),
            budget=data.get('budget'),
            special_requirements=data.get('special_requirements'),
            order_date=datetime.strptime(data['order_date'], '%Y-%m-%d').date(),
            delivery_date=datetime.strptime(data['delivery_date'], '%Y-%m-%d').date(),
            status='pending'
        )
        
        db.session.add(order)
        db.session.commit()
        
        return api_response(
            status="success",
            message="Order created successfully!",
            data={
                "order_id": order.id,
                "customer_name": order.customer_name,
                "status": order.status,
                "delivery_date": order.delivery_date.isoformat()
            },
            code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Failed to create order: {str(e)}",
            code=500
        )


@orders_bp.route('/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    """Get all orders for user"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Order.query.filter_by(user_id=user_id)
    
    if status:
        query = query.filter_by(status=status)
    
    query = query.order_by(Order.delivery_date.desc())
    items, total_count, total_pages = Helpers.paginate_query(query, page)
    
    orders_data = [{
        "id": order.id,
        "customer_name": order.customer_name,
        "cake_type": order.cake_type,
        "flavor": order.flavor,
        "status": order.status,
        "order_date": order.order_date.isoformat(),
        "delivery_date": order.delivery_date.isoformat(),
        "estimated_profit": order.estimated_profit,
        "actual_profit": order.actual_profit,
        "selling_price": order.selling_price
    } for order in items]
    
    pagination_data = Helpers.generate_pagination_data(
        orders_data, total_count, total_pages, page
    )
    
    return api_response(
        status="success",
        data=pagination_data
    )


@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order details"""
    order = Order.query.get(order_id)
    
    if not order:
        return api_response(
            status="error",
            message="Order not found",
            code=404
        )
    
    # Get order items
    items_data = []
    total_cost = 0
    for item in order.items:
        cost = item.cost
        total_cost += cost
        items_data.append({
            "ingredient_id": item.ingredient_id,
            "ingredient_name": item.ingredient.name,
            "quantity_used": item.quantity_used,
            "unit": item.unit,
            "cost": cost
        })
    
    return api_response(
        status="success",
        data={
            "id": order.id,
            "customer_name": order.customer_name,
            "customer_phone": order.customer_phone,
            "customer_email": order.customer_email,
            "cake_type": order.cake_type,
            "cake_weight": order.cake_weight,
            "flavor": order.flavor,
            "theme": order.theme,
            "status": order.status,
            "order_date": order.order_date.isoformat(),
            "delivery_date": order.delivery_date.isoformat(),
            "special_requirements": order.special_requirements,
            "items": items_data,
            "estimated_ingredient_cost": order.estimated_ingredient_cost,
            "actual_cost": order.actual_cost,
            "selling_price": order.selling_price,
            "estimated_profit": order.estimated_profit,
            "actual_profit": order.actual_profit,
            "notes": order.notes
        }
    )


@orders_bp.route('/<int:order_id>/estimate', methods=['POST'])
@require_json
@validate_inputs(['ingredients'])
def estimate_order_cost(order_id):
    """Estimate order cost based on ingredients used"""
    order = Order.query.get(order_id)
    
    if not order:
        return api_response(
            status="error",
            message="Order not found",
            code=404
        )
    
    data = request.get_json()
    ingredients = data['ingredients']  # List of {ingredient_id, quantity_used}
    
    try:
        total_cost = 0
        
        for item in ingredients:
            ingredient = Ingredient.query.get(item['ingredient_id'])
            if not ingredient:
                continue
            
            cost = ingredient.get_cost_used(item['quantity_used'])
            total_cost += cost
            
            # Add order item
            order_item = OrderItem(
                order_id=order_id,
                ingredient_id=item['ingredient_id'],
                quantity_used=item['quantity_used'],
                unit=ingredient.unit,
                cost=cost
            )
            db.session.add(order_item)
        
        order.estimated_ingredient_cost = total_cost
        order.actual_cost = total_cost
        
        # Suggest selling price using AI
        ai_service = AIService()
        market_rate = order.budget or total_cost * 2
        
        suggested_price = CalculationService.suggest_selling_price(
            total_cost=total_cost,
            market_rate=market_rate,
            desired_margin=40
        )
        
        order.selling_price = suggested_price
        order.actual_profit = order.calculate_profit()
        
        db.session.commit()
        
        return api_response(
            status="success",
            message="Order estimated!",
            data={
                "estimated_ingredient_cost": round(total_cost, 2),
                "suggested_selling_price": round(suggested_price, 2),
                "suggested_profit": round(order.actual_profit, 2),
                "profit_margin": round(((suggested_price - total_cost) / suggested_price) * 100, 2)
            }
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Estimation failed: {str(e)}",
            code=500
        )


@orders_bp.route('/<int:order_id>/status', methods=['PUT'])
@require_json
@validate_inputs(['status'])
def update_order_status(order_id):
    """Update order status"""
    order = Order.query.get(order_id)
    
    if not order:
        return api_response(
            status="error",
            message="Order not found",
            code=404
        )
    
    data = request.get_json()
    valid_statuses = ['pending', 'accepted', 'in_progress', 'completed', 'cancelled']
    
    if data['status'] not in valid_statuses:
        return api_response(
            status="error",
            message=f"Invalid status. Use: {', '.join(valid_statuses)}",
            code=400
        )
    
    try:
        order.status = data['status']
        db.session.commit()
        
        return api_response(
            status="success",
            message=f"Order status updated to {data['status']}!",
            data={"order_id": order_id, "status": order.status}
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Update failed: {str(e)}",
            code=500
        )


@orders_bp.route('/<int:order_id>/finalize', methods=['POST'])
@require_json
def finalize_order(order_id):
    """Finalize order with actual costs and profits"""
    order = Order.query.get(order_id)
    
    if not order:
        return api_response(
            status="error",
            message="Order not found",
            code=404
        )
    
    data = request.get_json()
    
    try:
        if 'selling_price' in data:
            order.selling_price = data['selling_price']
        
        if 'actual_cost' in data:
            order.actual_cost = data['actual_cost']
        
        if 'notes' in data:
            order.notes = data['notes']
        
        order.calculate_profit()
        order.status = 'completed'
        
        db.session.commit()
        
        return api_response(
            status="success",
            message="Order finalized!",
            data={
                "order_id": order_id,
                "selling_price": order.selling_price,
                "actual_cost": order.actual_cost,
                "profit": order.actual_profit,
                "profit_margin": round(((order.actual_profit / order.selling_price) * 100), 2) if order.selling_price else 0
            }
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Finalization failed: {str(e)}",
            code=500
        )


@orders_bp.route('/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    """Cancel order"""
    order = Order.query.get(order_id)
    
    if not order:
        return api_response(
            status="error",
            message="Order not found",
            code=404
        )
    
    try:
        order.status = 'cancelled'
        db.session.commit()
        
        return api_response(
            status="success",
            message="Order cancelled!"
        )
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Cancel failed: {str(e)}",
            code=500
        )
