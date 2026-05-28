from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False) # Format: YYYY-MM-DD
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'income' or 'expense'
    notes = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'date': self.date,
            'category': self.category,
            'type': self.type,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
