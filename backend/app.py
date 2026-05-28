from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from config import Config

def create_app():
    try:
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
    except Exception as e:
        # Create a dummy app to return the error
        error_app = Flask(__name__)
        @error_app.route('/api/health', defaults={'path': ''})
        @error_app.route('/<path:path>')
        def error_handler(path):
            import traceback
            return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500
        return error_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
