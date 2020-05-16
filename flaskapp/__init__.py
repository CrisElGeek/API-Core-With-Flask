from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
# Configurations
app.config.from_object('config')
db = MySQL(app)

from flaskapp.controllers.users.users import users

app.register_blueprint(users)