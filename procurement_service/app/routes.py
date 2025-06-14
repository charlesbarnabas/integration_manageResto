from flask import Blueprint, render_template, request, jsonify, abort
from flask_graphql import GraphQLView
from app.graphql_schema import schema
from app.models import ProcurementOrder
from app import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# RESTful API endpoints for procurement orders

@main.route('/api/procurement', methods=['GET'])
def get_orders():
    orders = ProcurementOrder.query.all()
    result = []
    for order in orders:
        result.append({
            'id': order.id,
            'ingredient_name': order.ingredient_name,
            'quantity_ordered': order.quantity_ordered,
            'supplier': order.supplier,
            'status': order.status,
            'order_date': order.order_date.isoformat() if order.order_date else None
        })
    return jsonify(result)

@main.route('/api/procurement/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = ProcurementOrder.query.get_or_404(order_id)
    result = {
        'id': order.id,
        'ingredient_name': order.ingredient_name,
        'quantity_ordered': order.quantity_ordered,
        'supplier': order.supplier,
        'status': order.status,
        'order_date': order.order_date.isoformat() if order.order_date else None
    }
    return jsonify(result)

@main.route('/api/procurement', methods=['POST'])
def create_order():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    try:
        ingredient_name = data['ingredient_name']
        quantity_ordered = data['quantity_ordered']
        supplier = data['supplier']
        status = data.get('status', 'pending')
        order_date_str = data['order_date']
        order_date = datetime.fromisoformat(order_date_str)
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400

    new_order = ProcurementOrder(
        ingredient_name=ingredient_name,
        quantity_ordered=quantity_ordered,
        supplier=supplier,
        status=status,
        order_date=order_date
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created', 'id': new_order.id}), 201

@main.route('/api/procurement/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = ProcurementOrder.query.get_or_404(order_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    try:
        order.ingredient_name = data.get('ingredient_name', order.ingredient_name)
        order.quantity_ordered = data.get('quantity_ordered', order.quantity_ordered)
        order.supplier = data.get('supplier', order.supplier)
        order.status = data.get('status', order.status)
        order_date_str = data.get('order_date')
        if order_date_str:
            order.order_date = datetime.fromisoformat(order_date_str)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    db.session.commit()
    return jsonify({'message': 'Order updated'})

@main.route('/api/procurement/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = ProcurementOrder.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'})

# GraphQL endpoint
main.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)