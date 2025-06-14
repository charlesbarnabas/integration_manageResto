from . import db

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))

class MenuIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    ingredient_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

    menu = db.relationship('Menu', backref=db.backref('ingredients', lazy=True))
