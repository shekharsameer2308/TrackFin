from flask import Blueprint, request, jsonify
from models import db, Goal
from services.auth import token_required

goals_bp = Blueprint('goals', __name__)

@goals_bp.route('/', methods=['GET'])
@token_required
def get_goals(current_user):
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return jsonify([g.to_dict() for g in goals]), 200

@goals_bp.route('/', methods=['POST'])
@token_required
def create_goal(current_user):
    data = request.json
    if not data or not data.get('name') or not data.get('target_amount'):
        return jsonify({"error": "Missing name or target_amount"}), 400
        
    goal = Goal(
        user_id=current_user.id,
        name=data['name'],
        target_amount=float(data['target_amount']),
        current_amount=float(data.get('current_amount', 0.0)),
        deadline=data.get('deadline')
    )
    db.session.add(goal)
    db.session.commit()
    return jsonify(goal.to_dict()), 201

@goals_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_goal(current_user, id):
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first()
    if not goal:
        return jsonify({"error": "Goal not found"}), 404
        
    data = request.json
    if 'current_amount' in data:
        goal.current_amount = float(data['current_amount'])
    if 'target_amount' in data:
        goal.target_amount = float(data['target_amount'])
        
    db.session.commit()
    return jsonify(goal.to_dict()), 200

@goals_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_goal(current_user, id):
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first()
    if not goal:
        return jsonify({"error": "Goal not found"}), 404
        
    db.session.delete(goal)
    db.session.commit()
    return jsonify({"message": "Goal deleted successfully"}), 200
