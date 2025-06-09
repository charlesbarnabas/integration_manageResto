from app import db
from datetime import datetime

class ProcurementOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(100), nullable=False)
    quantity_ordered = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    supplier = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Order {self.ingredient_name} - {self.quantity_ordered}>'
