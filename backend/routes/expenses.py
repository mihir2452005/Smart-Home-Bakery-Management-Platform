"""
Expenses Routes
Track and manage business expenses
"""

from flask import Blueprint, request
from datetime import datetime, date
from models.database import db, Expense
from utils.helpers import api_response, require_json, validate_inputs, Helpers

expenses_bp = Blueprint('expenses', __name__)


@expenses_bp.route('/<int:user_id>', methods=['GET'])
def get_expenses(user_id):
    """Get expenses for user"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    
    query = Expense.query.filter_by(user_id=user_id).order_by(Expense.expense_date.desc())
    
    if category:
        query = query.filter_by(category=category)
    
    items, total_count, total_pages = Helpers.paginate_query(query, page)
    
    expenses_data = [{
        "id": exp.id,
        "category": exp.category,
        "amount": exp.amount,
        "description": exp.description,
        "expense_date": exp.expense_date.isoformat(),
        "payment_method": exp.payment_method
    } for exp in items]
    
    pagination_data = Helpers.generate_pagination_data(
        expenses_data, total_count, total_pages, page
    )
    
    return api_response(
        status="success",
        data=pagination_data
    )


@expenses_bp.route('/', methods=['POST'])
@require_json
@validate_inputs(['user_id', 'category', 'amount', 'expense_date'])
def add_expense():
    """
    Add new expense
    
    Required fields:
    - user_id: User ID
    - category: Expense category
    - amount: Amount in INR
    - expense_date: Date of expense (YYYY-MM-DD)
    """
    data = request.get_json()
    
    try:
        expense = Expense(
            user_id=data['user_id'],
            category=data['category'],
            amount=data['amount'],
            description=data.get('description'),
            expense_date=datetime.strptime(data['expense_date'], '%Y-%m-%d').date(),
            payment_method=data.get('payment_method'),
            receipt_url=data.get('receipt_url')
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return api_response(
            status="success",
            message="Expense added!",
            data={
                "id": expense.id,
                "category": expense.category,
                "amount": expense.amount
            },
            code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Failed to add expense: {str(e)}",
            code=500
        )


@expenses_bp.route('/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    """Get expense details"""
    expense = Expense.query.get(expense_id)
    
    if not expense:
        return api_response(
            status="error",
            message="Expense not found",
            code=404
        )
    
    return api_response(
        status="success",
        data={
            "id": expense.id,
            "category": expense.category,
            "amount": expense.amount,
            "description": expense.description,
            "expense_date": expense.expense_date.isoformat(),
            "payment_method": expense.payment_method,
            "receipt_url": expense.receipt_url
        }
    )


@expenses_bp.route('/<int:expense_id>', methods=['PUT'])
@require_json
def update_expense(expense_id):
    """Update expense"""
    expense = Expense.query.get(expense_id)
    
    if not expense:
        return api_response(
            status="error",
            message="Expense not found",
            code=404
        )
    
    data = request.get_json()
    
    if 'category' in data:
        expense.category = data['category']
    if 'amount' in data:
        expense.amount = data['amount']
    if 'description' in data:
        expense.description = data['description']
    if 'payment_method' in data:
        expense.payment_method = data['payment_method']
    
    try:
        db.session.commit()
        return api_response(
            status="success",
            message="Expense updated!"
        )
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Update failed: {str(e)}",
            code=500
        )


@expenses_bp.route('/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete expense"""
    expense = Expense.query.get(expense_id)
    
    if not expense:
        return api_response(
            status="error",
            message="Expense not found",
            code=404
        )
    
    try:
        db.session.delete(expense)
        db.session.commit()
        return api_response(
            status="success",
            message="Expense deleted!"
        )
    except Exception as e:
        db.session.rollback()
        return api_response(
            status="error",
            message=f"Delete failed: {str(e)}",
            code=500
        )
