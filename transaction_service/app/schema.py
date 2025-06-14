import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import db, Order, OrderItem, Transaction, ProcurementTransaction

# === Type Definitions ===
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

# === Query ===
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_orders = SQLAlchemyConnectionField(OrderType.connection)
    all_order_items = SQLAlchemyConnectionField(OrderItemType.connection)
    all_transactions = SQLAlchemyConnectionField(TransactionType.connection)
    all_procurement_transactions = SQLAlchemyConnectionField(ProcurementTransactionType.connection)

# === Input Type for Nested Mutation ===
class OrderItemInput(graphene.InputObjectType):
    menu_item_id = graphene.Int(required=True)
    menu_item_name = graphene.String(required=True)
    quantity = graphene.Int(required=True)
    price = graphene.Float(required=True)

# === Mutations ===
class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_name = graphene.String(required=True)

    order = graphene.Field(lambda: OrderType)

    def mutate(self, info, customer_name):
        order = Order(customer_name=customer_name)
        db.session.add(order)
        db.session.commit()
        return CreateOrder(order=order)

class CreateOrderItem(graphene.Mutation):
    class Arguments:
        order_id = graphene.Int(required=True)
        menu_item_id = graphene.Int(required=True)
        menu_item_name = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        price = graphene.Float(required=True)

    order_item = graphene.Field(lambda: OrderItemType)

    def mutate(self, info, order_id, menu_item_id, menu_item_name, quantity, price):
        item = OrderItem(
            order_id=order_id,
            menu_item_id=menu_item_id,
            menu_item_name=menu_item_name,
            quantity=quantity,
            price=price
        )
        db.session.add(item)
        db.session.commit()
        return CreateOrderItem(order_item=item)

class CreateTransaction(graphene.Mutation):
    class Arguments:
        order_id = graphene.Int(required=True)
        amount = graphene.Float(required=True)
        method = graphene.String(required=True)
        status = graphene.String(required=True)

    transaction = graphene.Field(lambda: TransactionType)

    def mutate(self, info, order_id, amount, method, status):
        tx = Transaction(order_id=order_id, amount=amount, method=method, status=status)
        db.session.add(tx)
        db.session.commit()
        return CreateTransaction(transaction=tx)

class CreateProcurementTransaction(graphene.Mutation):
    class Arguments:
        procurement_order_id = graphene.Int(required=True)
        ingredient_name = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        supplier = graphene.String(required=True)
        amount = graphene.Float(required=True)
        status = graphene.String(required=True)

    procurement_transaction = graphene.Field(lambda: ProcurementTransactionType)

    def mutate(self, info, procurement_order_id, ingredient_name, quantity, supplier, amount, status):
        tx = ProcurementTransaction(
            procurement_order_id=procurement_order_id,
            ingredient_name=ingredient_name,
            quantity=quantity,
            supplier=supplier,
            amount=amount,
            status=status
        )
        db.session.add(tx)
        db.session.commit()
        return CreateProcurementTransaction(procurement_transaction=tx)

class CreateOrderWithItems(graphene.Mutation):
    class Arguments:
        customer_name = graphene.String(required=True)
        items = graphene.List(OrderItemInput, required=True)

    order = graphene.Field(lambda: OrderType)
    order_items = graphene.List(lambda: OrderItemType)

    def mutate(self, info, customer_name, items):
        # Create order
        order = Order(customer_name=customer_name)
        db.session.add(order)
        db.session.commit()

        created_items = []
        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item.menu_item_id,
                menu_item_name=item.menu_item_name,
                quantity=item.quantity,
                price=item.price
            )
            db.session.add(order_item)
            created_items.append(order_item)

        db.session.commit()
        return CreateOrderWithItems(order=order, order_items=created_items)

# === Root Mutation ===
class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    create_order_item = CreateOrderItem.Field()
    create_transaction = CreateTransaction.Field()
    create_procurement_transaction = CreateProcurementTransaction.Field()
    create_order_with_items = CreateOrderWithItems.Field()

# === Final Schema ===
schema = graphene.Schema(query=Query, mutation=Mutation)
