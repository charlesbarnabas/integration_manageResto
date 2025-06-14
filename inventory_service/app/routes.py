from flask import Blueprint, render_template, jsonify, request
from flask_graphql import GraphQLView
from app.schema import schema
from app.models import Inventory, Ingredient
from flask import current_app
from sqlalchemy import create_engine, text
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/ingredient', methods=['GET'])
def get_inventories():
    ingredient_items = Ingredient.query.all()
    result = []
    for item in ingredient_items:
        result.append({
            'id': item.id,
            'name': item.name,
            'quantity': item.quantity,
            'minimum_stock_level': item.minimum_stock_level,
            'reorder_quantity': item.reorder_quantity,
            'unit_of_measure': item.unit_of_measure
        })
    return jsonify(result)

@main.route('/api/ingredient', methods=['POST'])
def add_inventory():
    data = request.get_json()
    name = data.get('name')
    quantity = data.get('quantity')
    minimum_stock_level = data.get('minimumStockLevel')
    reorder_quantity = data.get('reorderQuantity')
    unit_of_measure = data.get('unitOfMeasure')

    if not name or quantity is None or not unit_of_measure:
        return jsonify({'error': 'Data tidak lengkap'}), 400

    new_item = Ingredient(
        name=name,
        quantity=quantity,
        minimum_stock_level=minimum_stock_level,
        reorder_quantity=reorder_quantity,
        unit_of_measure=unit_of_measure
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Bahan berhasil ditambahkan', 'id': new_item.id}), 201

@main.route('/api/ingredient/<string:id>', methods=['PUT'])
def update_inventory(id):
    data = request.get_json()
    ingredient = Ingredient.query.get(id)
    if not ingredient:
        return jsonify({'error': 'Bahan tidak ditemukan'}), 404

    ingredient.name = data.get('name', ingredient.name)
    ingredient.quantity = data.get('quantity', ingredient.quantity)
    ingredient.minimum_stock_level = data.get('minimumStockLevel', ingredient.minimum_stock_level)
    ingredient.reorder_quantity = data.get('reorderQuantity', ingredient.reorder_quantity)
    ingredient.unit_of_measure = data.get('unitOfMeasure', ingredient.unit_of_measure)

    db.session.commit()
    return jsonify({'message': 'Bahan berhasil diperbarui'}), 200

@main.route('/api/menu_ingredients')
def get_menu_ingredients():
    # Connect to menu_service database directly
    menu_db_uri = 'sqlite:///../menu_service/menu.db'  # Adjust path as needed
    engine = create_engine(menu_db_uri)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DISTINCT ingredient_name FROM menu_ingredient"))
        ingredients = [row[0] for row in result]
    return jsonify({'ingredients': ingredients})
# GraphQL endpoint
main.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)

