import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
try:
    from models import db
    from config import Config
except ImportError as e:
    # We will let the app run and return the error on the root
    db = None
    Config = None
    import_error = str(e)
else:
    import_error = None

def create_app():
    if import_error:
        error_app = Flask(__name__)
        @error_app.route('/api/health', defaults={'path': ''})
        @error_app.route('/<path:path>')
        def handle_import_error(path):
            return jsonify({"error": f"Import Error: {import_error}"}), 500
        return error_app
        
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
