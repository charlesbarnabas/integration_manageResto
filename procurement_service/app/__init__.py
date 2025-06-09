from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_graphql import GraphQLView

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    from app.schema import schema

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True  # Enable GraphiQL interface
        )
    )

    with app.app_context():
        from app import models
        db.create_all()

    return app
