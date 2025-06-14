from flask import Flask
from flask_cors import CORS
from .models import db
from .routes import bp, register_graphql

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  
    CORS(app)
    db.init_app(app)
    app.register_blueprint(bp)
    register_graphql(app)
    return app
