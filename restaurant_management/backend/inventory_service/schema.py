import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import InventoryItem
from database import db
from datetime import datetime

class InventoryItemObject(SQLAlchemyObjectType):
    class Meta:
        model = InventoryItem
        interfaces = (graphene.relay.Node,)

class CreateInventoryItem(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        unit = graphene.String(required=True)

    item = graphene.Field(lambda: InventoryItemObject)

    def mutate(self, info, name, quantity, unit):
        item = InventoryItem(
            name=name,
            quantity=quantity,
            unit=unit,
            updated_at=datetime.utcnow()
        )
        db.session.add(item)
        db.session.commit()
        return CreateInventoryItem(item=item)

class UpdateInventoryItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    item = graphene.Field(lambda: InventoryItemObject)

    def mutate(self, info, id, quantity):
        item = InventoryItem.query.get(id)
        if item:
            item.quantity = quantity
            item.updated_at = datetime.utcnow()
            db.session.commit()
        return UpdateInventoryItem(item=item)

class Mutation(graphene.ObjectType):
    create_inventory_item = CreateInventoryItem.Field()
    update_inventory_item = UpdateInventoryItem.Field()

class Query(graphene.ObjectType):
    all_items = graphene.List(InventoryItemObject)

    def resolve_all_items(self, info):
        return InventoryItem.query.all()

schema = graphene.Schema(query=Query, mutation=Mutation)
