from app import db

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Inventory {self.name}>'

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    minimum_stock_level = db.Column(db.Integer, nullable=True)  # Level Stok Minimum
    reorder_quantity = db.Column(db.Integer, nullable=True)     # Kuantitas Pemesanan Ulang
    unit_of_measure = db.Column(db.String(50), nullable=True)   # Satuan Ukur

    def __repr__(self):
        return f'<Ingredient {self.name}>'

