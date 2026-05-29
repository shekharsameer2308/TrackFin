from flask import Blueprint, request, jsonify, current_app
from models import db, User
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing credentials'}), 400
        
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
        
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing credentials'}), 400
        
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
        
    token = jwt.encode({
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({'token': token}), 200

@auth_bp.route('/guest', methods=['POST'])
def guest_login():
    import uuid
    # Create a unique guest username
    guest_username = f"guest_{uuid.uuid4().hex[:8]}"
    guest_password = uuid.uuid4().hex
    
    user = User(username=guest_username)
    user.set_password(guest_password)
    db.session.add(user)
    db.session.commit()
    
    token = jwt.encode({
        'user_id': user.id,
        'username': guest_username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1) # 1 day expiry for guests
    }, current_app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({'token': token, 'username': guest_username}), 200
