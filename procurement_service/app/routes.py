from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime

main = Blueprint('main', __name__)

# Simpan data di list (sementara), atau gunakan database
orders = []

@main.route('/')
def index():
    return render_template('index.html', orders=orders)

@main.route('/create_order', methods=['POST'])
def create_order():
    ingredient_name = request.form.get('ingredient_name')
    quantity = request.form.get('quantity')
    supplier = request.form.get('supplier')
    
    if not ingredient_name or not quantity or not supplier:
        return "Please fill all fields", 400

    order = {
        'ingredient_name': ingredient_name,
        'quantity': quantity,
        'supplier': supplier,
        'status': 'Pending',
        'order_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    orders.append(order)
    return redirect(url_for('main.index'))
