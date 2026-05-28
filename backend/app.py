from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Transaction
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    @app.route('/api/transactions', methods=['GET'])
    def get_transactions():
        transactions = Transaction.query.order_by(Transaction.date.desc()).all()
        return jsonify([t.to_dict() for t in transactions]), 200

    @app.route('/api/transactions', methods=['POST'])
    def add_transaction():
        data = request.json
        if not data or not all(k in data for k in ('amount', 'date', 'category', 'type')):
            return jsonify({"error": "Missing required fields"}), 400
            
        try:
            transaction = Transaction(
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

    @app.route('/api/transactions/<int:id>', methods=['DELETE'])
    def delete_transaction(id):
        transaction = Transaction.query.get(id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
            
        db.session.delete(transaction)
        db.session.commit()
        return jsonify({"message": "Transaction deleted successfully"}), 200
        
    @app.route('/api/summary', methods=['GET'])
    def get_summary():
        transactions = Transaction.query.all()
        income = sum(t.amount for t in transactions if t.type == 'income')
        expenses = sum(t.amount for t in transactions if t.type == 'expense')
        
        # Category breakdown for expenses
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

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
