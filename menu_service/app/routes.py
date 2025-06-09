from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import requests
from flask_graphql import GraphQLView
from .graphql_schema import schema
from .models import Menu, MenuIngredient
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
        ingredient_names = request.form.getlist('ingredient_name')
        quantities = request.form.getlist('quantity')
        new_menu = Menu(name=name, description=description, price=price)
        db.session.add(new_menu)
        db.session.commit()
        for ing_name, qty in zip(ingredient_names, quantities):
            menu_ingredient = MenuIngredient(
                menu_id=new_menu.id,
                ingredient_name=ing_name,
                quantity=float(qty)
            )
            db.session.add(menu_ingredient)
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

# RESTful API endpoints for menus

@main.route('/api/menus', methods=['GET'])
def get_menus():
    menus = Menu.query.all()
    result = []
    for menu in menus:
        ingredients = [
            {
                'ingredient_name': ing.ingredient_name,
                'quantity': ing.quantity
            } for ing in menu.ingredients
        ]
        result.append({
            'id': menu.id,
            'name': menu.name,
            'description': menu.description,
            'price': menu.price,
            'ingredients': ingredients
        })
    return jsonify(result)

@main.route('/api/menus/<int:menu_id>', methods=['GET'])
def get_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    ingredients = [
        {
            'ingredient_name': ing.ingredient_name,
            'quantity': ing.quantity
        } for ing in menu.ingredients
    ]
    result = {
        'id': menu.id,
        'name': menu.name,
        'description': menu.description,
        'price': menu.price,
        'ingredients': ingredients
    }
    return jsonify(result)

@main.route('/api/menus', methods=['POST'])
def create_menu():
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        ingredients = data.get('ingredients', [])
        new_menu = Menu(name=name, description=description, price=price)
        db.session.add(new_menu)
        db.session.commit()
        for ing in ingredients:
            menu_ingredient = MenuIngredient(
                menu_id=new_menu.id,
                ingredient_name=ing['ingredient_name'],
                quantity=ing['quantity']
            )
            db.session.add(menu_ingredient)
        db.session.commit()
        return jsonify({'message': 'Menu created', 'id': new_menu.id}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@main.route('/api/menus/<int:menu_id>', methods=['PUT'])
def update_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    data = request.get_json()
    menu.name = data.get('name', menu.name)
    menu.description = data.get('description', menu.description)
    menu.price = data.get('price', menu.price)
    # Update ingredients
    ingredients = data.get('ingredients', [])
    # Remove existing ingredients
    MenuIngredient.query.filter_by(menu_id=menu.id).delete()
    for ing in ingredients:
        menu_ingredient = MenuIngredient(
            menu_id=menu.id,
            ingredient_name=ing['ingredient_name'],
            quantity=ing['quantity']
        )
        db.session.add(menu_ingredient)
    db.session.commit()
    return jsonify({'message': 'Menu updated'})

@main.route('/api/menus/<int:menu_id>', methods=['DELETE'])
def delete_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    # Delete ingredients first
    MenuIngredient.query.filter_by(menu_id=menu.id).delete()
    db.session.delete(menu)
    db.session.commit()
    return jsonify({'message': 'Menu deleted'})

# API endpoint to get unique list of all ingredients used in menus
@main.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = db.session.query(MenuIngredient.ingredient_name).distinct().all()
    ingredient_list = [ing[0] for ing in ingredients]
    return jsonify({'ingredients': ingredient_list})

# GraphQL endpoint
main.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)
