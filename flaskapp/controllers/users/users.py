from flask import jsonify, Blueprint, request
from flaskapp.models.middleware import Models
from flaskapp.libs.form_validation import Validate
from argon2 import PasswordHasher
from flaskapp.libs.jwt import JWTAuth

users = Blueprint('users', __name__)
get_params = {
  "database": "users u",
  "fields": {
    "id": {"field": "u.id", "protected": True},
    "first_name": {"field": "u.first_name"},
    "last_name": {"field": "u.last_name"},
    "email": {"field": "u.email"},
    "phone": {"field": "u.phone"},
    "status_id": {"field": "u.status_id"},
    "password": {"field": "u.password", "secured": True},
    "role_id": {"field": "u.role_id"},
    "permissions": {"field": "u.permissions"}
  }
}

rules = {
  "first_name": "required|max:100",
  "last_name": "required|max:100",
  "email": "required|max:150|email|unique:users:email",
  "phone": "required|max:20|numeric|min:10|unique:users:phone",
  "status_id": "required|min_value:1|max:4|numeric",
  "role_id": "required|min_value:1|max:11|numeric"
}

@users.route('/api/v1/users/', methods=['GET'])
def UserList():
  results = Models(get_params)
  res = results.Get()
  return jsonify(res), res["code"]

@users.route('/api/v1/users/<int:id>', methods=['GET'])
def UserView(id):
  results = Models(get_params)
  res = results.Get(id)
  return jsonify(res), res["code"]

@users.route('/api/v1/users/add', methods=['POST'])
def UserAdd():
  data = request.get_json()
  results = Models(get_params, data)
  payload = results.Params(True)
  rules["password"] = "required|min:6"
  errors = Validate().execute(payload, rules)
  if len(errors) == 0:
    ph = PasswordHasher()
    payload["password"][0] = ph.hash(payload["password"][0])
    r = results.Post(payload)
    # TODO: DEFINIR LOS PERMISOS PARA ASIGNAR ROLES
    # TODO: SOLO DEVOLVER EL JWT CUANDO ES USUARIO NUEVO QUE SE REGISTRA POR SI MISMO
    auth = JWTAuth(payload, r["data"]["id"]).encode()
    return jsonify({"bearer": auth}), r["code"]
  else:
    return jsonify(errors), 400
