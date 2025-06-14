from app import db
from sqlalchemy import Column, Integer, String, DateTime

class ProcurementOrder(db.Model):
    __tablename__ = 'procurement_orders'
    id = Column(Integer, primary_key=True)
    ingredient_name = Column(String, nullable=False)
    quantity_ordered = Column(Integer, nullable=False)
    supplier = Column(String, nullable=False)
    status = Column(String, default='pending')  # e.g., pending, approved, rejected, delivered
    order_date = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<ProcurementOrder(id={self.id}, ingredient_name='{self.ingredient_name}')>" 