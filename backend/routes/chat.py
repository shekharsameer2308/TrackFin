from flask import Blueprint, request, jsonify
from models import db, Transaction
from services.auth import token_required

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
@token_required
def chat_with_ai(current_user):
    data = request.json
    message = data.get('message', '').lower()
    
    # 1. Fetch user data to make the AI "aware" of context
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    total_spent = sum(t.amount for t in transactions if t.type == 'expense')
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    
    # 2. Mock AI Logic (Rule-based parsing)
    reply = ""
    
    if "how much" in message and "spend" in message:
        reply = f"Based on your recent data, you've spent a total of ${total_spent:.2f}. "
        if total_spent > total_income and total_income > 0:
            reply += "You're currently spending more than you're earning. Time to cut back!"
        elif total_spent == 0:
            reply += "You haven't logged any expenses yet!"
        else:
            reply += "Looks like you're keeping it under control."
            
    elif "food" in message or "eating" in message or "restaurant" in message:
        food_spent = sum(t.amount for t in transactions if t.type == 'expense' and t.category == 'Food')
        reply = f"You've spent ${food_spent:.2f} on Food & Dining. That's about {((food_spent/total_spent)*100) if total_spent > 0 else 0:.1f}% of your total expenses."
        
    elif "advice" in message or "help" in message:
        reply = "I'd recommend keeping your fixed subscriptions under 30% of your income. Also, try to set a Savings Goal in the dashboard if you haven't already!"
        
    elif "hello" in message or "hi" in message:
        reply = f"Hello {current_user.username}! I'm your TrackFin AI Advisor. Ask me anything about your spending."
        
    else:
        reply = "I'm still learning! (Mock AI Mode). Ask me 'How much did I spend?' or 'Give me financial advice'."
        
    # In production, this would be:
    # response = openai.ChatCompletion.create(messages=[{"role": "user", "content": message}, ...])
    # reply = response.choices[0].message.content

    return jsonify({"reply": reply}), 200
