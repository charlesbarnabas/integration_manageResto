from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS more generically
    CORS(app)
    
    db.init_app(app)
    
    # Import and register GraphQL schema
    from .graphql_schema import schema
    from flask_graphql import GraphQLView
    
    # Add GraphQL endpoint with batch and middleware
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True,  # Enable GraphiQL interface
            batch=True,     # Enable batch requests
            middleware=[]   # No middleware needed for now
        )
    )
    
    from app.routes import procurement_bp
    app.register_blueprint(procurement_bp)
    
    return app 