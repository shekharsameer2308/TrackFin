from flask import Blueprint, request, jsonify
from models import db, Transaction
from services.auth import token_required
from services.categorizer import smart_categorize

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
    if not data or not all(k in data for k in ('amount', 'date', 'type')):
        return jsonify({"error": "Missing required fields"}), 400
        
    notes = data.get('notes', '')
    
    # Run through smart categorizer if category isn't explicitly defined or is 'Other'
    category = data.get('category')
    is_recurring = False
    
    if not category or category == 'Other':
        category, is_recurring = smart_categorize(notes)
    else:
        # Just check if it's recurring even if category is manually set
        _, is_recurring = smart_categorize(notes)
        
    try:
        transaction = Transaction(
            user_id=current_user.id,
            amount=float(data['amount']),
            date=data['date'],
            category=category,
            type=data['type'],
            notes=notes,
            is_recurring=is_recurring
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

@transactions_bp.route('/ocr', methods=['POST'])
@token_required
def mock_ocr(current_user):
    # In production, send image payload to Google Cloud Vision or AWS Textract
    # Here we mock the AI response
    data = request.json
    return jsonify({
        "status": "success",
        "extracted_data": {
            "merchant": "Whole Foods Market",
            "amount": 45.20,
            "date": "2026-05-28",
            "suggested_category": "Food"
        }
    }), 200

@transactions_bp.route('/voice', methods=['POST'])
@token_required
def mock_voice(current_user):
    # In production, send audio buffer to OpenAI Whisper or Google Speech-to-Text
    # Here we mock the NLP extraction ("I just spent 15 dollars on an uber")
    data = request.json
    text = data.get("text", "").lower()
    
    # Mock NLP extraction logic
    amount = 15.00 if "15" in text else 0.00
    category, is_recurring = smart_categorize(text)
    
    return jsonify({
        "status": "success",
        "extracted_data": {
            "merchant": "Uber" if "uber" in text else "Unknown",
            "amount": amount,
            "type": "expense",
            "category": category
        }
    }), 200
