from graphene import ObjectType, String, Int, Schema, Field, List, ID, Mutation, Boolean
from graphene_sqlalchemy import SQLAlchemyObjectType
from datetime import datetime
import requests

from app.models import ProcurementOrder

# GraphQL Types
class ProcurementOrderType(SQLAlchemyObjectType):
    class Meta:
        model = ProcurementOrder

# GraphQL Queries
class Query(ObjectType):
    procurement_orders = List(ProcurementOrderType)
    procurement_order = Field(ProcurementOrderType, id=ID())
    ingredients = List(String) # To fetch ingredient names from inventory_service

    def resolve_procurement_orders(self, info):
        return ProcurementOrder.query.all()

    def resolve_procurement_order(self, info, id):
        return ProcurementOrder.query.get(id)

    def resolve_ingredients(self, info):
        inventory_service_url = "http://localhost:5002/graphql" 
        query = """
        query {
            ingredients {
                name
            }
        }
        """
        try:
            response = requests.post(inventory_service_url, json={'query': query})
            response.raise_for_status()
            data = response.json()
            return [ingredient['name'] for ingredient in data.get('data', {}).get('ingredients', [])]
        except Exception as e:
            print(f"Error fetching ingredients from inventory_service: {e}")
            return []

# GraphQL Mutations
class CreateProcurementOrder(Mutation):
    class Arguments:
        ingredient_name = String(required=True)
        quantity_ordered = Int(required=True)
        supplier = String(required=True)

    procurement_order = Field(ProcurementOrderType)

    def mutate(self, info, ingredient_name, quantity_ordered, supplier):
        order = ProcurementOrder(
            ingredient_name=ingredient_name,
            quantity_ordered=quantity_ordered,
            supplier=supplier,
            order_date=datetime.now()
        )
        from app import db #
        db.session.add(order)
        db.session.commit()
        return CreateProcurementOrder(procurement_order=order)

class UpdateProcurementOrderStatus(Mutation):
    class Arguments:
        id = ID(required=True)
        status = String(required=True)

    procurement_order = Field(ProcurementOrderType)

    def mutate(self, info, id, status):
        from app import db # Import db here to avoid circular dependency
        order = ProcurementOrder.query.get(id)
        if order:
            order.status = status
            db.session.commit()
            return UpdateProcurementOrderStatus(procurement_order=order)
        return None

class Mutation(ObjectType):
    create_procurement_order = CreateProcurementOrder.Field()
    update_procurement_order_status = UpdateProcurementOrderStatus.Field()

schema = Schema(query=Query, mutation=Mutation) 