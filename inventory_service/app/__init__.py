from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import CORS
import os

# Initialize extensions
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Initialize CORS
    
    # Database configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
