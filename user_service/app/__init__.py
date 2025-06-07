from flask import Flask, render_template, request, redirect, url_for, flash
from flask_graphql import GraphQLView
from flask_login import LoginManager, current_user, login_user, logout_user
from .extensions import db
from .schema import schema
from .models import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'  # Wajib untuk Flask-Login

    db.init_app(app)
    login_manager.init_app(app)

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True  # Enable GraphiQL interface
        )
    )

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:  # Tanpa hash
                login_user(user)
                return redirect(url_for('index'))
            flash('Invalid username or password')
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if not username or not password:
                flash('Please fill in all fields')
                return redirect(url_for('register'))
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists')
                return redirect(url_for('register'))
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    with app.app_context():
        db.create_all()

    return app