from flask import Blueprint, render_template, jsonify
from flask_graphql import GraphQLView
from app.schema import schema
from app.models import Inventory

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

# GraphQL endpoint
main.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)
