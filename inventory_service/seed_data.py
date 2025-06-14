from app import create_app, db
from app.models import Inventory

app = create_app()

def seed_data():
    with app.app_context():
        # Clear existing data
        Inventory.query.delete()
        # Add sample inventory items
        items = [
            Inventory(name='Tomato', quantity=100, minimum_stock_level=20, reorder_quantity=50, unit_of_measure='kg', price=1.5),
            Inventory(name='Cheese', quantity=50, minimum_stock_level=10, reorder_quantity=30, unit_of_measure='kg', price=5.0),
            Inventory(name='Flour', quantity=200, minimum_stock_level=50, reorder_quantity=100, unit_of_measure='kg', price=0.8),
        ]
        db.session.bulk_save_objects(items)
        db.session.commit()
        print("Seed data added successfully.")

if __name__ == '__main__':
    seed_data()
