from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    from .routes import main
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    
    # Enable CORS for all origins
    CORS(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
