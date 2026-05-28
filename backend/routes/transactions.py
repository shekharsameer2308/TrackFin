from flask import Blueprint, request, jsonify
from models import db, Transaction
from services.auth import token_required

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions', methods=['GET'])
@token_required
def get_transactions(current_user):
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return jsonify([t.to_dict() for t in transactions]), 200

@transactions_bp.route('/transactions', methods=['POST'])
@token_required
def add_transaction(current_user):
    data = request.json
    if not data or not all(k in data for k in ('amount', 'date', 'category', 'type')):
        return jsonify({"error": "Missing required fields"}), 400
        
    try:
        transaction = Transaction(
            user_id=current_user.id,
            amount=float(data['amount']),
            date=data['date'],
            category=data['category'],
            type=data['type'],
            notes=data.get('notes', '')
        )
        db.session.add(transaction)
        db.session.commit()
        return jsonify(transaction.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@transactions_bp.route('/transactions/<int:id>', methods=['DELETE'])
@token_required
def delete_transaction(current_user, id):
    transaction = Transaction.query.filter_by(id=id, user_id=current_user.id).first()
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
        
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction deleted successfully"}), 200

@transactions_bp.route('/summary', methods=['GET'])
@token_required
def get_summary(current_user):
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    income = sum(t.amount for t in transactions if t.type == 'income')
    expenses = sum(t.amount for t in transactions if t.type == 'expense')
    
    categories = {}
    for t in transactions:
        if t.type == 'expense':
            categories[t.category] = categories.get(t.category, 0) + t.amount
            
    return jsonify({
        "income": income,
        "expenses": expenses,
        "net": income - expenses,
        "expensesByCategory": categories
    }), 200
