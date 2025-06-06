from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    # Menggunakan konfigurasi dari config.py
    app.config.from_object(Config)

    # Inisialisasi ekstensi
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Register blueprint
    from .routes import bp
    app.register_blueprint(bp)

    # Buat instance folder jika belum ada
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app 