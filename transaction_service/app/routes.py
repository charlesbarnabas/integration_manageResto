from flask_graphql import GraphQLView
from flask import Blueprint, request, jsonify, render_template
from .models import db, Order, OrderItem, Transaction, ProcurementTransaction
from .schema import schema
import requests

bp = Blueprint('transaction', __name__, static_folder='static', template_folder='templates')

MENU_SERVICE_URL = 'http://menu_service:5001'  # adjust as needed

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
    result = [{
        'id': order.id,
        'customer_name': order.customer_name,
        'status': order.status,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for order in orders]
    return jsonify(result)

@bp.route('/api/transaction/orders', methods=['POST'])
def create_order():
    data = request.json
    customer_name = data.get('customer_name')
    items = data.get('items', [])
    if not customer_name or not items:
        return jsonify({'error': 'Customer name and items are required'}), 400

    order = Order(customer_name=customer_name)
    db.session.add(order)
    db.session.flush()  # get order.id before commit

    total = 0
    for item in items:
        menu_item_id = item['menu_item_id']
        quantity = item['quantity']

        try:
            resp = requests.get(f"{MENU_SERVICE_URL}/api/menus/{menu_item_id}", timeout=5)
            resp.raise_for_status()
            menu_data = resp.json()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to fetch menu item {menu_item_id}: {str(e)}'}), 500

        price = menu_data.get('price')
        if price is None:
            db.session.rollback()
            return jsonify({'error': f'Price not found for menu item {menu_item_id}'}), 500

        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=menu_item_id,
            menu_item_name=menu_data.get('name', ''),
            quantity=quantity,
            price=price
        )
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
    if order.status == 'paid':
        return jsonify({'message': 'Order already paid'}), 400

    total = sum(item.price * item.quantity for item in order.order_items)
    transaction = Transaction(
        order_id=order.id,
        amount=total,
        method=method,
        status='completed'
    )
    db.session.add(transaction)
    order.status = 'paid'
    db.session.commit()

    return jsonify({
        'transaction_id': transaction.id,
        'amount': total,
        'status': 'completed'
    })

@bp.route('/api/transaction/transactions', methods=['GET'])
def list_transactions():
    transactions = Transaction.query.join(Order).add_columns(
        Transaction.id,
        Transaction.order_id,
        Transaction.amount,
        Transaction.method,
        Transaction.status,
        Transaction.created_at,
        Order.customer_name,
        Order.status.label('order_status')
    ).all()

    result = [{
        'id': t.id,
        'order_id': t.order_id,
        'amount': t.amount,
        'method': t.method,
        'status': t.status,
        'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'customer_name': t.customer_name,
        'order_status': t.order_status
    } for (_, t) in enumerate(transactions)]

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
    # Data lokal
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
    # Data eksternal
    try:
        ext_resp = requests.get('https://inventory-service-gacor-production.up.railway.app/')
        procurement_resp = requests.get('http://procurement_service:5003/api/procurement')
        procurement_data = procurement_resp.json() if procurement_resp.status_code == 200 else []
        if ext_resp.status_code == 200:
            ext_data = ext_resp.json()
            for ext in ext_data:
                # Cari supplier dan status dari procurement berdasarkan ingredient_name
                matched = next((p for p in procurement_data if (p.get('ingredient_name') or '').lower() == (ext.get('name') or '').lower()), None)
                supplier = matched['supplier'] if matched else ext.get('supplier', '')
                status = matched['status'] if matched else ext.get('status', '')
                result.append({
                    'id': f"{ext.get('id', '')}",
                    'procurement_order_id': ext.get('item_code', ''),
                    'ingredient_name': ext.get('name', ''),
                    'quantity': ext.get('stock_quantity', ''),
                    'supplier': supplier,
                    'amount': f"Rp{int(ext.get('unit_price', 0)):,}".replace(",", "."),
                    'status': status,
                    'created_at': ext.get('created_at', '')
                })
    except Exception as e:
        pass  # Bisa tambahkan logging jika perlu
    return jsonify(result)

def register_graphql(app):
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    )
