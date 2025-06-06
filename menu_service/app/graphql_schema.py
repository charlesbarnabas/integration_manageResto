import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Menu as MenuModel
from . import db

# Object Type untuk Menu
class Menu(SQLAlchemyObjectType):
    class Meta:
        model = MenuModel

# Query semua menu
class Query(graphene.ObjectType):
    all_menus = graphene.List(Menu)

    def resolve_all_menus(self, info):
        return MenuModel.query.all()

# Mutation untuk membuat menu baru
class CreateMenu(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        description = graphene.String()

    menu = graphene.Field(lambda: Menu)

    def mutate(self, info, name, price, description=None):
        menu = MenuModel(name=name, price=price, description=description)
        db.session.add(menu)
        db.session.commit()
        return CreateMenu(menu=menu)

# ✅ Mutation untuk update menu
class UpdateMenu(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        price = graphene.Float()
        description = graphene.String()

    menu = graphene.Field(lambda: Menu)

    def mutate(self, info, id, name=None, price=None, description=None):
        menu = MenuModel.query.get(id)
        if not menu:
            raise Exception("Menu not found")

        if name is not None:
            menu.name = name
        if price is not None:
            menu.price = price
        if description is not None:
            menu.description = description

        db.session.commit()
        return UpdateMenu(menu=menu)

# ✅ Mutation untuk delete menu
class DeleteMenu(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        menu = MenuModel.query.get(id)
        if not menu:
            return DeleteMenu(ok=False)
        db.session.delete(menu)
        db.session.commit()
        return DeleteMenu(ok=True)

# Gabungkan semua mutation
class Mutation(graphene.ObjectType):
    create_menu = CreateMenu.Field()
    update_menu = UpdateMenu.Field()
    delete_menu = DeleteMenu.Field()

# Skema utama
schema = graphene.Schema(query=Query, mutation=Mutation)
