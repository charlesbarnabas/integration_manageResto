from graphene import ObjectType, String, Int, Schema, Field, List, ID, Mutation
from graphene_sqlalchemy import SQLAlchemyObjectType
from datetime import datetime
from app.models import ProcurementOrder

# GraphQL Type
class ProcurementOrderType(SQLAlchemyObjectType):
    class Meta:
        model = ProcurementOrder

# Queries
class Query(ObjectType):
    procurement_orders = List(ProcurementOrderType)

    def resolve_procurement_orders(self, info):
        return ProcurementOrder.query.all()

# Mutations
class CreateProcurementOrder(Mutation):
    class Arguments:
        ingredientName = String(required=True)
        quantityOrdered = Int(required=True)
        supplier = String()

    id = ID()
    ingredient_name = String()
    quantity_ordered = Int()
    status = String()
    order_date = String()
    supplier = String()

    def mutate(self, info, ingredientName, quantityOrdered, supplier=None):
        from app import db
        order = ProcurementOrder(
            ingredient_name=ingredientName,
            quantity_ordered=quantityOrdered,
            status='pending',
            order_date=datetime.utcnow(),
            supplier=supplier
        )
        db.session.add(order)
        db.session.commit()
        return CreateProcurementOrder(
            id=order.id,
            ingredient_name=order.ingredient_name,
            quantity_ordered=order.quantity_ordered,
            status=order.status,
            order_date=str(order.order_date),
            supplier=order.supplier
        )

class UpdateProcurementOrderStatus(Mutation):
    class Arguments:
        id = ID(required=True)
        status = String(required=True)

    id = ID()
    status = String()

    def mutate(self, info, id, status):
        from app import db
        order = ProcurementOrder.query.get(id)
        if order:
            order.status = status
            db.session.commit()
            return UpdateProcurementOrderStatus(id=order.id, status=order.status)
        return None

# Mutation Root
class Mutation(ObjectType):
    create_procurement_order = CreateProcurementOrder.Field()
    update_procurement_order_status = UpdateProcurementOrderStatus.Field()

# Final schema
schema = Schema(query=Query, mutation=Mutation)
