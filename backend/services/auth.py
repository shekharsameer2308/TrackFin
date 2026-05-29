import jwt
from functools import wraps
from flask import request, jsonify, current_app
from models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
            
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                # VERCEL STATELESS FIX: If the SQLite DB was wiped by a cold start,
                # recreate the user seamlessly since their JWT is cryptographically valid!
                from models import db
                username = data.get('username', f'user_{data["user_id"]}')
                current_user = User(id=data['user_id'], username=username)
                db.session.add(current_user)
                db.session.commit()
                
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
            
        return f(current_user, *args, **kwargs)
        
    return decorated
