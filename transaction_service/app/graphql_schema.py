import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import db, Order, OrderItem, Transaction, ProcurementTransaction

class OrderItemType(SQLAlchemyObjectType):
    class Meta:
        model = OrderItem
        interfaces = (graphene.relay.Node, )

class TransactionType(SQLAlchemyObjectType):
    class Meta:
        model = Transaction
        interfaces = (graphene.relay.Node, )

class OrderType(SQLAlchemyObjectType):
    class Meta:
        model = Order
        interfaces = (graphene.relay.Node, )

class ProcurementTransactionType(SQLAlchemyObjectType):
    class Meta:
        model = ProcurementTransaction
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_orders = SQLAlchemyConnectionField(OrderType.connection)
    all_transactions = SQLAlchemyConnectionField(TransactionType.connection)
    all_order_items = SQLAlchemyConnectionField(OrderItemType.connection)
    all_procurement_transactions = SQLAlchemyConnectionField(ProcurementTransactionType.connection)

schema = graphene.Schema(query=Query)
