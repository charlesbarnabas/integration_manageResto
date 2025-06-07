from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import requests
from flask_graphql import GraphQLView
from .graphql_schema import schema
from .models import Menu
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def menu_list():
    menus = Menu.query.all()
    return render_template('menu_list.html', menus=menus)

@main.route('/add', methods=['GET', 'POST'])
def add_menu():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        new_menu = Menu(name=name, description=description, price=price)
        db.session.add(new_menu)
        db.session.commit()
        return redirect(url_for('main.menu_list'))
    return render_template('add_menu.html')

@main.route('/inventory')
def inventory_list():
    try:
        response = requests.get('http://localhost:5002/api/inventory')
        response.raise_for_status()
        inventory_data = response.json()
    except Exception as e:
        inventory_data = []
    return render_template('inventory_list.html', inventory=inventory_data)

# GraphQL endpoint
main.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)
