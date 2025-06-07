import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import User
from .extensions import db
from flask_login import login_user, logout_user

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_all_users(self, info):
        return User.query.all()

    def resolve_user(self, info, id):
        return User.query.get(id)

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(lambda: UserType)

    def mutate(self, info, username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user)

class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(lambda: UserType)

    def mutate(self, info, username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Tanpa hash
            login_user(user)
            return LoginUser(user=user)
        return None

class LogoutUser(graphene.Mutation):
    success = graphene.Boolean()

    def mutate(self, info):
        logout_user()
        return LogoutUser(success=True)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)