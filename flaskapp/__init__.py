from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
# Configurations
app.config.from_object('config')
db = MySQL(app)

from flaskapp.controllers.access.login import access
from flaskapp.controllers.users.users import users
from flaskapp.controllers.roles.roles import roles

app.register_blueprint(access)
app.register_blueprint(users)
app.register_blueprint(roles)