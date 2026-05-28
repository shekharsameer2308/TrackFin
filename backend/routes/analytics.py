from flask import Blueprint, jsonify
from models import Transaction
from services.auth import token_required
import datetime
from collections import defaultdict

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/health', methods=['GET'])
@token_required
def get_health_score(current_user):
    # Calculate a simple health score 0-100
    # Rule 1: Saving more than spending -> high score
    # Rule 2: High proportion of essential (housing, food) is okay, high entertainment is penalty
    
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    if not transactions:
        return jsonify({"score": 50, "status": "Neutral", "message": "Add transactions to see your health score."}), 200
        
    income = sum(t.amount for t in transactions if t.type == 'income')
    expenses = sum(t.amount for t in transactions if t.type == 'expense')
    
    if income == 0:
        return jsonify({"score": 20, "status": "Critical", "message": "No income detected! Watch your burn rate."}), 200
        
    savings_ratio = (income - expenses) / income
    
    base_score = 50
    score_modifier = int(savings_ratio * 100) # e.g. 20% savings = +20 points
    
    final_score = min(max(base_score + score_modifier, 0), 100)
    
    status = "Excellent" if final_score >= 80 else "Good" if final_score >= 60 else "Warning" if final_score >= 40 else "Critical"
    
    return jsonify({
        "score": final_score,
        "status": status,
        "savings_ratio": round(savings_ratio * 100, 1)
    }), 200

@analytics_bp.route('/subscriptions', methods=['GET'])
@token_required
def get_subscriptions(current_user):
    # Get all recurring expenses
    recurring_txs = Transaction.query.filter_by(user_id=current_user.id, is_recurring=True, type='expense').all()
    
    subs_map = {}
    for tx in recurring_txs:
        # Group by category or notes to estimate monthly burn
        key = tx.notes.lower() if tx.notes else tx.category
        if key not in subs_map or tx.date > subs_map[key]['last_date']:
            subs_map[key] = {
                "name": tx.notes or tx.category,
                "amount": tx.amount,
                "category": tx.category,
                "last_date": tx.date
            }
            
    monthly_burn = sum(sub['amount'] for sub in subs_map.values())
    
    return jsonify({
        "monthly_burn": monthly_burn,
        "active_subscriptions": list(subs_map.values())
    }), 200

@analytics_bp.route('/predict', methods=['GET'])
@token_required
def predict_balance(current_user):
    # Predict balance for next 30 days based on average daily burn rate over last 30 days
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=30)
    
    # Query transactions from last 30 days
    recent_txs = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= thirty_days_ago.isoformat()
    ).all()
    
    expenses_30d = sum(t.amount for t in recent_txs if t.type == 'expense')
    daily_burn_rate = expenses_30d / 30.0 if recent_txs else 0
    
    # Simple prediction: Next 30 days will have the same burn rate
    return jsonify({
        "daily_burn_rate": round(daily_burn_rate, 2),
        "predicted_30d_expense": round(daily_burn_rate * 30, 2)
    }), 200
