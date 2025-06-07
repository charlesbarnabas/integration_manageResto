from flask import Blueprint, render_template
from flask_graphql import GraphQLView
from app.schema import schema

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# GraphQL endpoint
main.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)
