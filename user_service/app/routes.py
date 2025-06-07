import requests
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # ... (tidak berubah)
    pass

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user
from .models import User
from . import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Tanpa hash
            login_user(user)
            return redirect('http://localhost:5001/')
        flash('Invalid username or password')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# ✅ Tambahkan route ini untuk integrasi ke menu_service
@bp.route('/menus')
@login_required
def user_menus():
    try:
        response = requests.post(
            'http://localhost:5001/graphql',  # ganti sesuai URL service kamu
            json={"query": "{ all_menus { id name description price } }"},
            headers={'Content-Type': 'application/json'}
        )
        data = response.json()
        menus = data.get("data", {}).get("all_menus", [])
        return render_template('user_menu.html', menus=menus)
    except Exception as e:
        flash(f"Gagal memuat menu: {str(e)}", 'error')
        return render_template('user_menu.html', menus=[])
