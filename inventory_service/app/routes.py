from flask import Blueprint, render_template, jsonify
from flask_graphql import GraphQLView
from app.schema import schema
from app.models import Inventory
from flask import current_app
from sqlalchemy import create_engine, text

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/inventory')
def get_inventory():
    inventory_items = Inventory.query.all()
    inventory_list = []
    for item in inventory_items:
        inventory_list.append({
            'id': item.id,
            'name': item.name,
            'quantity': item.quantity,
            'price': item.price
        })
    return jsonify(inventory_list)

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

