from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import Procurement, Supplier
from datetime import datetime
import requests
from config import Config
from flask_graphql import GraphQLView
from .graphql_schema import schema

procurement_bp = Blueprint('procurement', __name__)

# Add GraphQL endpoint
procurement_bp.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)

# Supplier routes
@procurement_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'contact_person': s.contact_person,
        'phone': s.phone,
        'email': s.email,
        'address': s.address
    } for s in suppliers])

@procurement_bp.route('/suppliers', methods=['POST'])
def create_supplier():
    data = request.get_json()
    supplier = Supplier(
        name=data['name'],
        contact_person=data.get('contact_person'),
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address')
    )
    db.session.add(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier created successfully', 'id': supplier.id}), 201

# Procurement routes
@procurement_bp.route('/procurements', methods=['GET'])
def get_procurements():
    procurements = Procurement.query.all()
    return jsonify([{
        'id': p.id,
        'supplier_id': p.supplier_id,
        'item_name': p.item_name,
        'quantity': p.quantity,
        'unit_price': p.unit_price,
        'total_price': p.total_price,
        'status': p.status,
        'order_date': p.order_date.isoformat(),
        'expected_delivery_date': p.expected_delivery_date.isoformat() if p.expected_delivery_date else None,
        'actual_delivery_date': p.actual_delivery_date.isoformat() if p.actual_delivery_date else None,
        'notes': p.notes
    } for p in procurements])

@procurement_bp.route('/procurements', methods=['POST'])
def create_procurement():
    data = request.get_json()
    procurement = Procurement(
        supplier_id=data['supplier_id'],
        item_name=data['item_name'],
        quantity=data['quantity'],
        unit_price=data['unit_price'],
        total_price=data['quantity'] * data['unit_price'],
        expected_delivery_date=datetime.fromisoformat(data['expected_delivery_date']) if 'expected_delivery_date' in data else None,
        notes=data.get('notes')
    )
    db.session.add(procurement)
    db.session.commit()
    return jsonify({'message': 'Procurement created successfully', 'id': procurement.id}), 201

@procurement_bp.route('/procurements/<int:id>/status', methods=['PUT'])
def update_procurement_status(id):
    data = request.get_json()
    procurement = Procurement.query.get_or_404(id)
    
    procurement.status = data['status']
    if data['status'] == 'received':
        procurement.actual_delivery_date = datetime.utcnow()
        # Update inventory through inventory service
        try:
            response = requests.post(
                f"{Config.INVENTORY_SERVICE_URL}/inventory/add",
                json={
                    'item_name': procurement.item_name,
                    'quantity': procurement.quantity
                }
            )
            if response.status_code != 200:
                return jsonify({'error': 'Failed to update inventory'}), 500
        except requests.RequestException:
            return jsonify({'error': 'Failed to connect to inventory service'}), 500
    
    db.session.commit()
    return jsonify({'message': 'Procurement status updated successfully'})

@procurement_bp.route('/', methods=['GET'])
def index():
    procurements = Procurement.query.all()
    # Convert datetime objects to string for JSON serialization if not already handled by jsonify
    procurement_data = [{
        'id': p.id,
        'supplier_id': p.supplier_id,
        'item_name': p.item_name,
        'quantity': p.quantity,
        'unit_price': p.unit_price,
        'total_price': p.total_price,
        'status': p.status,
        'order_date': p.order_date.isoformat(),
        'expected_delivery_date': p.expected_delivery_date.isoformat() if p.expected_delivery_date else None,
        'actual_delivery_date': p.actual_delivery_date.isoformat() if p.actual_delivery_date else None,
        'notes': p.notes
    } for p in procurements]
    return render_template('index.html', requests=procurement_data) 