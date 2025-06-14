from graphene import ObjectType, String, Int, Schema, Field, List, ID, Mutation, Boolean
from graphene_sqlalchemy import SQLAlchemyObjectType
from app import db
from app.models import Inventory, Ingredient
import requests
from app.config import Config

# GraphQL Types
class InventoryType(SQLAlchemyObjectType):
    class Meta:
        model = Inventory

class IngredientType(SQLAlchemyObjectType):
    class Meta:
        model = Ingredient

    minimum_stock_level = Int()
    reorder_quantity = Int()
    unit_of_measure = String()

# GraphQL Queries
class Query(ObjectType):
    inventory = List(InventoryType)
    ingredients = List(IngredientType)

    def resolve_inventory(self, info):
        return Inventory.query.all()

    def resolve_ingredients(self, info):
        return Ingredient.query.all()

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

# Helper function to trigger procurement service
def trigger_procurement(item_name, quantity):
    url = Config.PROCUREMENT_SERVICE_URL
    payload = {
        'item_name': item_name,
        'quantity': quantity
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Procurement triggered for {item_name}, quantity {quantity}")
        return True
    except Exception as e:
        print(f"Error triggering procurement: {e}")
        return False

# GraphQL Mutations
class AddIngredient(Mutation):
    class Arguments:
        name = String(required=True)
        quantity = Int(required=True)
        minimum_stock_level = Int()
        reorder_quantity = Int()
        unit_of_measure = String()

    id = ID()
    name = String()
    quantity = Int()
    minimum_stock_level = Int()
    reorder_quantity = Int()
    unit_of_measure = String()

    def mutate(self, info, name, quantity, minimum_stock_level=None, reorder_quantity=None, unit_of_measure=None):
        ingredient = Ingredient(
            name=name,
            quantity=quantity,
            minimum_stock_level=minimum_stock_level,
            reorder_quantity=reorder_quantity,
            unit_of_measure=unit_of_measure
        )
        db.session.add(ingredient)
        db.session.commit()
        return AddIngredient(
            id=ingredient.id,
            name=ingredient.name,
            quantity=ingredient.quantity,
            minimum_stock_level=ingredient.minimum_stock_level,
            reorder_quantity=ingredient.reorder_quantity,
            unit_of_measure=ingredient.unit_of_measure
        )

class UpdateIngredient(Mutation):
    class Arguments:
        id = ID(required=True)
        name = String()
        quantity = Int()
        minimum_stock_level = Int()
        reorder_quantity = Int()
        unit_of_measure = String()

    id = ID()
    name = String()
    quantity = Int()
    minimum_stock_level = Int()
    reorder_quantity = Int()
    unit_of_measure = String()

    def mutate(self, info, id, name=None, quantity=None, minimum_stock_level=None, reorder_quantity=None, unit_of_measure=None):
        ingredient = Ingredient.query.get(id)
        if ingredient:
            if name is not None:
                ingredient.name = name
            if quantity is not None:
                ingredient.quantity = quantity
            if minimum_stock_level is not None:
                ingredient.minimum_stock_level = minimum_stock_level
            if reorder_quantity is not None:
                ingredient.reorder_quantity = reorder_quantity
            if unit_of_measure is not None:
                ingredient.unit_of_measure = unit_of_measure
            db.session.commit()
            # Check stock level and trigger procurement if below threshold
            threshold = 10
            if ingredient.quantity < threshold:
                triggered = trigger_procurement(ingredient.name, threshold * 2)  # Order double threshold
                if not triggered:
                    print(f"Failed to trigger procurement for {ingredient.name}")
            return UpdateIngredient(
                id=ingredient.id,
                name=ingredient.name,
                quantity=ingredient.quantity,
                minimum_stock_level=ingredient.minimum_stock_level,
                reorder_quantity=ingredient.reorder_quantity,
                unit_of_measure=ingredient.unit_of_measure
            )
        return None

class DeleteIngredient(Mutation):
    class Arguments:
        id = ID(required=True)

    success = Boolean()

    def mutate(self, info, id):
        ingredient = Ingredient.query.get(id)
        if ingredient:
            db.session.delete(ingredient)
            db.session.commit()
            return DeleteIngredient(success=True)
        return DeleteIngredient(success=False)

class AddItem(Mutation):
    class Arguments:
        name = String(required=True)
        quantity = Int(required=True)

    id = ID()
    name = String()
    quantity = Int()

    def mutate(self, info, name, quantity):
        item = Inventory(name=name, quantity=quantity)
        db.session.add(item)
        db.session.commit()
        return AddItem(
            id=item.id,
            name=item.name,
            quantity=item.quantity
        )

class UpdateItem(Mutation):
    class Arguments:
        id = ID(required=True)
        name = String(required=True)
        quantity = Int(required=True)

    id = ID()
    name = String()
    quantity = Int()

    def mutate(self, info, id, name, quantity):
        item = Inventory.query.get(id)
        if item:
            item.name = name
            item.quantity = quantity
            db.session.commit()
            return UpdateItem(
                id=item.id,
                name=item.name,
                quantity=item.quantity
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

    add_ingredient = AddIngredient.Field()
    update_ingredient = UpdateIngredient.Field()
    delete_ingredient = DeleteIngredient.Field()

# Create schema
schema = Schema(query=Query, mutation=Mutation)
