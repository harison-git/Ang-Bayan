from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate


# Specify the custom static URL path
custom_static_url_path = '/static'

app = Flask(__name__, static_url_path=custom_static_url_path)
bootstrap = Bootstrap(app)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Configure the database connection for SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cesu4.db'  # Use SQLite with a database file named 'cesu.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from wtforms import SelectField
from flask_wtf import FlaskForm


class Form(FlaskForm):
    program = SelectField('Program', choices=[])
    subprogram = SelectField('Sub-Program', choices=[])

from main.routes.indexRoute import index_route
from main.routes.dbModelRoute import dbModel_route
from main.routes.adminRoute import admin_route
from main.routes.randomForestRoute import randomForest_Route

app.register_blueprint(index_route)
app.register_blueprint(dbModel_route)
app.register_blueprint(admin_route)
app.register_blueprint(randomForest_Route)