from flask import Blueprint, request, jsonify, render_template
from .models import db, Order, OrderItem, Transaction, ProcurementTransaction
import requests

bp = Blueprint('transaction', __name__, static_folder='static', template_folder='templates')

MENU_SERVICE_URL = 'http://menu_service:5000'  # adjust as needed

# --- FRONTEND ROUTES ---
@bp.route('/orders')
def order_list_page():
    return render_template('order_list.html')

@bp.route('/transactions')
def transaction_list_page():
    return render_template('transaction_list.html')

# --- API ROUTES ---
@bp.route('/api/transaction/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    result = []
    for order in orders:
        result.append({
            'id': order.id,
            'customer_name': order.customer_name,
            'status': order.status,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(result)

@bp.route('/api/transaction/orders', methods=['POST'])
def create_order():
    data = request.json
    customer_name = data.get('customer_name')
    items = data.get('items', [])
    order = Order(customer_name=customer_name)
    db.session.add(order)
    db.session.commit()
    total = 0
    for item in items:
        menu_item_id = item['menu_item_id']
        quantity = item['quantity']
        # Fetch menu item details from Menu Service
        resp = requests.get(f"{MENU_SERVICE_URL}/menu/{menu_item_id}")
        if resp.status_code != 200:
            continue
        menu_data = resp.json()
        price = menu_data['price']
        order_item = OrderItem(order_id=order.id, menu_item_id=menu_item_id, menu_item_name=menu_data['name'], quantity=quantity, price=price)
        db.session.add(order_item)
        total += price * quantity
    db.session.commit()
    return jsonify({'order_id': order.id, 'total': total}), 201

@bp.route('/api/transaction/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.json
    status = data.get('status')
    order = Order.query.get_or_404(order_id)
    order.status = status
    db.session.commit()
    return jsonify({'message': 'Order status updated'})

@bp.route('/api/transaction/orders/<int:order_id>/pay', methods=['POST'])
def process_payment(order_id):
    data = request.json
    method = data.get('method')
    order = Order.query.get_or_404(order_id)
    total = sum([item.price * item.quantity for item in order.order_items])
    transaction = Transaction(order_id=order.id, amount=total, method=method, status='completed')
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'transaction_id': transaction.id, 'amount': total, 'status': 'completed'})

@bp.route('/api/transaction/transactions', methods=['GET'])
def list_transactions():
    transactions = Transaction.query.all()
    result = []
    for t in transactions:
        result.append({
            'id': t.id,
            'order_id': t.order_id,
            'amount': t.amount,
            'method': t.method,
            'status': t.status,
            'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(result)

@bp.route('/api/transaction/procurement', methods=['POST'])
def create_procurement_transaction():
    data = request.json
    procurement_order_id = data.get('procurement_order_id')
    ingredient_name = data.get('ingredient_name')
    quantity = data.get('quantity')
    supplier = data.get('supplier')
    amount = data.get('amount')
    status = data.get('status', 'completed')
    procurement_tx = ProcurementTransaction(
        procurement_order_id=procurement_order_id,
        ingredient_name=ingredient_name,
        quantity=quantity,
        supplier=supplier,
        amount=amount,
        status=status
    )
    db.session.add(procurement_tx)
    db.session.commit()
    return jsonify({'message': 'Procurement transaction recorded', 'id': procurement_tx.id}), 201

@bp.route('/api/transaction/procurement', methods=['GET'])
def list_procurement_transactions():
    txs = ProcurementTransaction.query.all()
    result = []
    for tx in txs:
        result.append({
            'id': tx.id,
            'procurement_order_id': tx.procurement_order_id,
            'ingredient_name': tx.ingredient_name,
            'quantity': tx.quantity,
            'supplier': tx.supplier,
            'amount': tx.amount,
            'status': tx.status,
            'created_at': tx.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(result)
