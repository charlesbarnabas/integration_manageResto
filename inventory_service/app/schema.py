from graphene import ObjectType, String, Int, Float, Schema, Field, List, ID, Mutation, Boolean
from graphene_sqlalchemy import SQLAlchemyObjectType
from app import db
from app.models import Inventory
import requests

# GraphQL Types
class InventoryType(SQLAlchemyObjectType):
    class Meta:
        model = Inventory
        # Remove interfaces as it's not needed for basic SQLAlchemy types

# GraphQL Queries
class Query(ObjectType):
    inventory = List(InventoryType)
    
    def resolve_inventory(self, info):
        return Inventory.query.all()

# Helper function to query menu_service GraphQL endpoint
def fetch_menu_data():
    url = 'http://localhost:5001/graphql'  # Assuming menu_service runs on port 5001
    query = '''
    query {
        allMenus {
            id
            name
            price
            description
        }
    }
    '''
    try:
        response = requests.post(url, json={'query': query})
        response.raise_for_status()
        data = response.json()
        return data.get('data', {}).get('allMenus', [])
    except Exception as e:
        print(f"Error fetching menu data: {e}")
        return []

# GraphQL Mutations
class AddItem(Mutation):
    class Arguments:
        name = String(required=True)
        quantity = Int(required=True)
        price = Float(required=True)
    
    id = ID()
    name = String()
    quantity = Int()
    price = Float()
    
    def mutate(self, info, name, quantity, price):
        # Fetch menu data from menu_service
        menu_data = fetch_menu_data()
        # Check if the name exists in menu_data
        menu_names = [menu['name'] for menu in menu_data]
        if name not in menu_names:
            raise Exception(f"Menu item '{name}' not found in menu_service.")
        
        item = Inventory(name=name, quantity=quantity, price=price)
        db.session.add(item)
        db.session.commit()
        return AddItem(
            id=item.id,
            name=item.name,
            quantity=item.quantity,
            price=item.price
        )

class UpdateItem(Mutation):
    class Arguments:
        id = ID(required=True)
        name = String(required=True)
        quantity = Int(required=True)
        price = Float(required=True)
    
    id = ID()
    name = String()
    quantity = Int()
    price = Float()
    
    def mutate(self, info, id, name, quantity, price):
        item = Inventory.query.get(id)
        if item:
            item.name = name
            item.quantity = quantity
            item.price = price
            db.session.commit()
            return UpdateItem(
                id=item.id,
                name=item.name,
                quantity=item.quantity,
                price=item.price
            )
        return None

class DeleteItem(Mutation):
    class Arguments:
        id = ID(required=True)
    
    success = Boolean()
    
    def mutate(self, info, id):
        item = Inventory.query.get(id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return DeleteItem(success=True)
        return DeleteItem(success=False)

class Mutation(ObjectType):
    add_item = AddItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()

# Create schema
schema = Schema(query=Query, mutation=Mutation)
