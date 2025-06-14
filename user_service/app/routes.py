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
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validasi password
        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('register.html')
        
        # Cek apakah username sudah ada
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return render_template('register.html')
        
        # Buat user baru
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('main.login'))
        
    return render_template('register.html')

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
            return redirect('http://localhost:5001/?user=' + user.username)
        flash('Invalid username or password')
    return render_template('login.html')

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('http://localhost:5000/login')

@bp.route('/menus')
@login_required
def user_menus():
    try:
        response = requests.post(
            'http://localhost:5001/graphql',  
            json={"query": "{ all_menus { id name description price } }"},
            headers={'Content-Type': 'application/json'}
        )
        data = response.json()
        menus = data.get("data", {}).get("all_menus", [])
        return render_template('menulist.html', menus=menus)
    except Exception as e:
        flash(f"Gagal memuat menu: {str(e)}", 'error')
        return render_template('menulist.html', menus=[])

@bp.route('/api/users/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return {'error': 'username and password required'}, 400
    if User.query.filter_by(username=username).first():
        return {'error': 'Username already exists'}, 400
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return {'message': 'Registration successful!'}, 201
