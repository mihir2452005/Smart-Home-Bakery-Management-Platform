"""
Dashboard Routes
Analytics and reporting
"""

from flask import Blueprint, request
from datetime import datetime, timedelta, date
from models.database import db, Order, Expense, ProfitReport, Recipe
from utils.helpers import api_response, Helpers

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/<int:user_id>/summary', methods=['GET'])
def get_dashboard_summary(user_id):
    """Get dashboard summary for user"""
    # Get date range (default: last 30 days)
    days = request.args.get('days', 30, type=int)
    start_date = date.today() - timedelta(days=days)
    
    # Get orders in date range
    completed_orders = Order.query.filter(
        Order.user_id == user_id,
        Order.status == 'completed',
        Order.delivery_date >= start_date
    ).all()
    
    total_orders = len(completed_orders)
    total_revenue = sum(order.selling_price or 0 for order in completed_orders)
    total_expenses = sum(order.actual_cost or 0 for order in completed_orders)
    total_profit = sum(order.actual_profit or 0 for order in completed_orders)
    
    # Get expenses
    expenses = Expense.query.filter(
        Expense.user_id == user_id,
        Expense.expense_date >= start_date
    ).all()
    total_business_expenses = sum(exp.amount for exp in expenses)
    
    net_profit = total_profit - total_business_expenses
    
    # Calculate average profit per cake
    avg_profit_per_cake = (total_profit / total_orders) if total_orders > 0 else 0
    
    # Get most selling flavor
    flavor_counts = {}
    for order in completed_orders:
        flavor = order.flavor or 'Unknown'
        flavor_counts[flavor] = flavor_counts.get(flavor, 0) + 1
    
    most_selling_flavor = max(flavor_counts, key=flavor_counts.get) if flavor_counts else None
    
    # Get top profit cake
    if completed_orders:
        top_profit_order = max(completed_orders, key=lambda x: x.actual_profit or 0)
        top_profit_cake = top_profit_order.cake_type
    else:
        top_profit_cake = None
    
    return api_response(
        status="success",
        data={
            "summary": {
                "period_days": days,
                "total_orders": total_orders,
                "total_revenue": round(total_revenue, 2),
                "total_expenses": round(total_expenses, 2),
                "total_business_expenses": round(total_business_expenses, 2),
                "total_profit": round(total_profit, 2),
                "net_profit": round(net_profit, 2),
                "average_profit_per_cake": round(avg_profit_per_cake, 2),
                "most_selling_flavor": most_selling_flavor,
                "top_profit_cake": top_profit_cake,
                "profit_status": Helpers.get_profit_status(
                    ((total_profit / total_revenue) * 100) if total_revenue > 0 else 0
                )
            },
            "profit_margin": round(((total_profit / total_revenue) * 100), 2) if total_revenue > 0 else 0,
            "avg_cake_price": round((total_revenue / total_orders), 2) if total_orders > 0 else 0,
            "avg_cake_cost": round((total_expenses / total_orders), 2) if total_orders > 0 else 0
        }
    )


@dashboard_bp.route('/<int:user_id>/daily-profit', methods=['GET'])
def get_daily_profit(user_id):
    """Get daily profit data"""
    days = request.args.get('days', 30, type=int)
    start_date = date.today() - timedelta(days=days)
    
    daily_data = {}
    
    # Get all completed orders
    orders = Order.query.filter(
        Order.user_id == user_id,
        Order.status == 'completed',
        Order.delivery_date >= start_date
    ).all()
    
    # Aggregate by date
    for order in orders:
        day = order.delivery_date.isoformat()
        if day not in daily_data:
            daily_data[day] = {
                'orders': 0,
                'revenue': 0,
                'expenses': 0,
                'profit': 0
            }
        
        daily_data[day]['orders'] += 1
        daily_data[day]['revenue'] += order.selling_price or 0
        daily_data[day]['expenses'] += order.actual_cost or 0
        daily_data[day]['profit'] += order.actual_profit or 0
    
    # Sort by date
    sorted_data = sorted(daily_data.items())
    
    return api_response(
        status="success",
        data=sorted_data
    )


@dashboard_bp.route('/<int:user_id>/recipe-performance', methods=['GET'])
def get_recipe_performance(user_id):
    """Get recipe performance metrics"""
    # Get top performing recipes
    recipes = Recipe.query.filter_by(user_id=user_id).order_by(
        Recipe.times_made.desc()
    ).limit(10).all()
    
    recipe_data = []
    for recipe in recipes:
        # Get orders for this recipe type
        orders = Order.query.filter(
            Order.user_id == user_id,
            Order.cake_type == recipe.cake_type,
            Order.status == 'completed'
        ).all()
        
        if orders:
            avg_profit = sum(order.actual_profit or 0 for order in orders) / len(orders)
            total_sold = len(orders)
            total_revenue = sum(order.selling_price or 0 for order in orders)
        else:
            avg_profit = 0
            total_sold = 0
            total_revenue = 0
        
        recipe_data.append({
            "recipe_id": recipe.id,
            "name": recipe.name,
            "cake_type": recipe.cake_type,
            "times_made": recipe.times_made,
            "rating": recipe.rating,
            "total_sold": total_sold,
            "total_revenue": round(total_revenue, 2),
            "avg_profit": round(avg_profit, 2)
        })
    
    return api_response(
        status="success",
        data=recipe_data
    )


@dashboard_bp.route('/<int:user_id>/expense-breakdown', methods=['GET'])
def get_expense_breakdown(user_id):
    """Get expense breakdown by category"""
    days = request.args.get('days', 30, type=int)
    start_date = date.today() - timedelta(days=days)
    
    expenses = Expense.query.filter(
        Expense.user_id == user_id,
        Expense.expense_date >= start_date
    ).all()
    
    # Group by category
    category_totals = {}
    for expense in expenses:
        category = expense.category
        category_totals[category] = category_totals.get(category, 0) + expense.amount
    
    total_expenses = sum(category_totals.values())
    
    breakdown = []
    for category, amount in category_totals.items():
        percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
        breakdown.append({
            "category": category,
            "amount": round(amount, 2),
            "percentage": round(percentage, 2)
        })
    
    # Sort by amount
    breakdown.sort(key=lambda x: x['amount'], reverse=True)
    
    return api_response(
        status="success",
        data={
            "total_expenses": round(total_expenses, 2),
            "breakdown": breakdown,
            "period_days": days
        }
    )


@dashboard_bp.route('/<int:user_id>/monthly-trend', methods=['GET'])
def get_monthly_trend(user_id):
    """Get monthly profit trend"""
    months = request.args.get('months', 6, type=int)
    
    monthly_data = []
    
    for i in range(months, 0, -1):
        # Calculate month start and end
        today = date.today()
        current_month_start = date(today.year, today.month, 1)
        month_start = current_month_start - timedelta(days=30*i)
        
        # Get month's next start
        if month_start.month == 12:
            month_end = date(month_start.year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = date(month_start.year, month_start.month + 1, 1) - timedelta(days=1)
        
        # Get orders for month
        orders = Order.query.filter(
            Order.user_id == user_id,
            Order.status == 'completed',
            Order.delivery_date >= month_start,
            Order.delivery_date <= month_end
        ).all()
        
        total_revenue = sum(order.selling_price or 0 for order in orders)
        total_profit = sum(order.actual_profit or 0 for order in orders)
        order_count = len(orders)
        
        monthly_data.append({
            "month": month_start.strftime('%Y-%m'),
            "revenue": round(total_revenue, 2),
            "profit": round(total_profit, 2),
            "orders": order_count
        })
    
    return api_response(
        status="success",
        data=monthly_data
    )


@dashboard_bp.route('/<int:user_id>/generate-report', methods=['POST'])
def generate_profit_report(user_id):
    """Generate detailed profit report"""
    report_date = date.today()
    
    # Get orders for today
    orders = Order.query.filter(
        Order.user_id == user_id,
        Order.status == 'completed',
        Order.delivery_date == report_date
    ).all()
    
    total_orders = len(orders)
    total_revenue = sum(order.selling_price or 0 for order in orders)
    total_expenses = sum(order.actual_cost or 0 for order in orders)
    total_profit = sum(order.actual_profit or 0 for order in orders)
    
    avg_profit = (total_profit / total_orders) if total_orders > 0 else 0
    
    # Most selling flavor
    flavor_counts = {}
    for order in orders:
        flavor = order.flavor or 'Unknown'
        flavor_counts[flavor] = flavor_counts.get(flavor, 0) + 1
    most_selling = max(flavor_counts, key=flavor_counts.get) if flavor_counts else None
    
    # Most profitable cake
    if orders:
        most_profitable = max(orders, key=lambda x: x.actual_profit or 0).cake_type
    else:
        most_profitable = None
    
    try:
        # Store report in database
        report = ProfitReport(
            user_id=user_id,
            report_date=report_date,
            total_orders=total_orders,
            total_revenue=total_revenue,
            total_ingredients_cost=total_expenses,
            total_profit=total_profit,
            average_profit_per_cake=avg_profit,
            most_selling_flavor=most_selling,
            most_profitable_flavor=most_profitable
        )
        
        db.session.add(report)
        db.session.commit()
        
        return api_response(
            status="success",
            message="Report generated!",
            data={
                "report_date": report_date.isoformat(),
                "total_orders": total_orders,
                "total_revenue": round(total_revenue, 2),
                "total_expenses": round(total_expenses, 2),
                "total_profit": round(total_profit, 2),
                "average_profit_per_cake": round(avg_profit, 2),
                "most_selling_flavor": most_selling,
                "most_profitable_cake": most_profitable
            }
        )
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Report generation failed: {str(e)}",
            code=500
        )
