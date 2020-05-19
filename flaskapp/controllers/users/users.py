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
    "permissions": {"field": "u.permissions"},
    "role_name": {"field": "r.role_name", "protected": True},
    "role_slug": {"field": "r.role_slug", "protected": True},
  },
  "joins": [
    {
      "table": "roles r",
      "match": ["r.id", "u.role_id"]
    }
  ]
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
  bearer = request.headers.get('Authorization')
  auth = JWTAuth(bearer).decode()
  if auth and auth["role"] <= 3:
    results = Models(get_params)
    res = results.Get()
    return jsonify(res), res["code"]
  else:
    return jsonify({
      "message": "You are not authorized to make this action"
    }), 401

@users.route('/api/v1/users/<int:id>', methods=['GET'])
def UserView(id):
  bearer = request.headers.get('Authorization')
  auth = JWTAuth(bearer).decode()
  if auth and auth["role"] >= 1:
    if auth["role"] > 3:
      id = auth["id"]
    results = Models(get_params)
    res = results.Get(id)
    return jsonify(res), res["code"]
  else:
    return jsonify({
      "message": "You are not authorized to make this action"
    }), 401

@users.route('/api/v1/users/add', methods=['POST'])
def UserAdd():
  bearer = request.headers.get('Authorization')
  auth = JWTAuth(bearer).decode()
  data = request.get_json()
  if not auth or auth["role"] > 3:
    data["role_id"] = 5
  results = Models(get_params, data)
  payload = results.Params(True)
  rules["password"] = "required|min:6"
  errors = Validate().execute(payload, rules)
  if len(errors) == 0:
    ph = PasswordHasher()
    payload["password"][0] = ph.hash(payload["password"][0])
    r = results.Post(payload)
    if not auth or auth["role"] > 3:
      bearer = JWTAuth(payload, r["data"]["id"]).encode()
      return jsonify({"bearer": bearer}), r["code"]
    else:
      return jsonify(r), r["code"]
  else:
    return jsonify(errors), 400

@users.route('/api/v1/users/update/<int:id>', methods=['PUT'])
def UserUpdate(id):
  bearer = request.headers.get('Authorization')
  auth = JWTAuth(bearer).decode()
  if auth and auth["role"] >= 1:
    data = request.get_json()
    results = Models(get_params, data)
    payload = results.Params()
    errors = Validate(id).execute(payload, rules)
    if len(errors) == 0:
      r = results.Put(id, payload)
      return jsonify(r), r["code"]
    else:
      return jsonify(errors), 400
  else:
    return jsonify({
      "message": "You are not authorized to make this action"
    }), 401