import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Procurement as ProcurementModel, Supplier as SupplierModel
from . import db

# Object Type untuk Supplier
class Supplier(SQLAlchemyObjectType):
    class Meta:
        model = SupplierModel

# Object Type untuk Procurement
class Procurement(SQLAlchemyObjectType):
    class Meta:
        model = ProcurementModel

# Query untuk Supplier dan Procurement
class Query(graphene.ObjectType):
    all_suppliers = graphene.List(Supplier)
    all_procurements = graphene.List(Procurement)
    supplier = graphene.Field(Supplier, id=graphene.ID(required=True))
    procurement = graphene.Field(Procurement, id=graphene.ID(required=True))

    def resolve_all_suppliers(self, info):
        return SupplierModel.query.all()

    def resolve_all_procurements(self, info):
        return ProcurementModel.query.all()

    def resolve_supplier(self, info, id):
        return SupplierModel.query.get(id)

    def resolve_procurement(self, info, id):
        return ProcurementModel.query.get(id)

# Mutation untuk membuat procurement baru
class CreateProcurement(graphene.Mutation):
    class Arguments:
        supplier_id = graphene.Int(required=True)
        item_name = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        unit_price = graphene.Float(required=True)
        total_price = graphene.Float(required=True)
        status = graphene.String()
        order_date = graphene.DateTime()
        expected_delivery_date = graphene.DateTime()
        actual_delivery_date = graphene.DateTime()
        notes = graphene.String()

    procurement = graphene.Field(lambda: Procurement)

    def mutate(self, info, supplier_id, item_name, quantity, unit_price, total_price, status=None, order_date=None, expected_delivery_date=None, actual_delivery_date=None, notes=None):
        procurement = ProcurementModel(
            supplier_id=supplier_id,
            item_name=item_name,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            status=status or 'pending',
            order_date=order_date,
            expected_delivery_date=expected_delivery_date,
            actual_delivery_date=actual_delivery_date,
            notes=notes
        )
        db.session.add(procurement)
        db.session.commit()
        return CreateProcurement(procurement=procurement)

# Mutation untuk update procurement
class UpdateProcurement(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        supplier_id = graphene.Int()
        item_name = graphene.String()
        quantity = graphene.Int()
        unit_price = graphene.Float()
        total_price = graphene.Float()
        status = graphene.String()
        order_date = graphene.DateTime()
        expected_delivery_date = graphene.DateTime()
        actual_delivery_date = graphene.DateTime()
        notes = graphene.String()

    procurement = graphene.Field(lambda: Procurement)

    def mutate(self, info, id, supplier_id=None, item_name=None, quantity=None, unit_price=None, total_price=None, status=None, order_date=None, expected_delivery_date=None, actual_delivery_date=None, notes=None):
        procurement = ProcurementModel.query.get(id)
        if not procurement:
            raise Exception("Procurement not found")
        if supplier_id is not None:
            procurement.supplier_id = supplier_id
        if item_name is not None:
            procurement.item_name = item_name
        if quantity is not None:
            procurement.quantity = quantity
        if unit_price is not None:
            procurement.unit_price = unit_price
        if total_price is not None:
            procurement.total_price = total_price
        if status is not None:
            procurement.status = status
        if order_date is not None:
            procurement.order_date = order_date
        if expected_delivery_date is not None:
            procurement.expected_delivery_date = expected_delivery_date
        if actual_delivery_date is not None:
            procurement.actual_delivery_date = actual_delivery_date
        if notes is not None:
            procurement.notes = notes
        db.session.commit()
        return UpdateProcurement(procurement=procurement)

# Mutation untuk delete procurement
class DeleteProcurement(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        procurement = ProcurementModel.query.get(id)
        if not procurement:
            return DeleteProcurement(ok=False)
        db.session.delete(procurement)
        db.session.commit()
        return DeleteProcurement(ok=True)

# Gabungkan semua mutation
class Mutation(graphene.ObjectType):
    create_procurement = CreateProcurement.Field()
    update_procurement = UpdateProcurement.Field()
    delete_procurement = DeleteProcurement.Field()

# Skema utama
schema = graphene.Schema(query=Query, mutation=Mutation) 