from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        from models import User, Transaction, Goal
        db.create_all()
        
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    # Register blueprints
    from routes.auth import auth_bp
    from routes.transactions import transactions_bp
    from routes.goals import goals_bp
    from routes.analytics import analytics_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(transactions_bp, url_prefix='/api')
    app.register_blueprint(goals_bp, url_prefix='/api/goals')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
