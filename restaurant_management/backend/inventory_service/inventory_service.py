from flask import Flask
from flask_graphql import GraphQLView
from database import db
from schema import schema
from flask import Flask, render_template


app = Flask(
    __name__,
    template_folder='../../frontend/templates',
    static_folder='../../frontend/static'
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def home():
    return render_template("inventory/inventory.html")

with app.app_context():
    db.create_all()

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
