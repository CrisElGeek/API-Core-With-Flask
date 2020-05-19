from flask import jsonify, Blueprint, request
from flaskapp.models.middleware import Models
from flaskapp.libs.form_validation import Validate
from flaskapp.libs.functions import Functions
from flaskapp.libs.jwt import JWTAuth

roles = Blueprint('roles', __name__)

get_params = {
  "database": "roles r",
  "fields": {
    "id": {"field": "r.id", "protected": True},
    "role_name": {"field": "r.role_name"},
    "role_slug": {"field": "r.role_slug"}
  }
}

rules = {
  "role_name": "required|max:50",
  "role_slug": "required|max:50|unique:roles:role_slug"
}

@roles.route('/api/v1/roles/', methods=['GET'])
def RoleList():
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

@roles.route('/api/v1/roles/<int:id>', methods=['GET'])
def RoleView(id):
  bearer = request.headers.get('Authorization')
  auth = JWTAuth(bearer).decode()
  if auth and auth["role"] <= 3:
    results = Models(get_params)
    res = results.Get(id)
    return jsonify(res), res["code"]
  else:
    return jsonify({
      "message": "You are not authorized to make this action"
    }), 401

@roles.route('/api/v1/roles/add', methods=['POST'])
def RoleAdd():
  bearer = request.headers.get('Authorization')
  auth = JWTAuth(bearer).decode()
  if auth and auth["role"] <= 3:
    data = request.get_json()
    slug = Functions().strToSlug(data["role_name"])
    data["role_slug"] = slug
    results = Models(get_params, data)
    payload = results.Params(True)
    errors = Validate().execute(payload, rules)
    if len(errors) == 0:
      r = results.Post(payload)
      return jsonify(r), r["code"]
    else:
      return jsonify(errors), 400
  else:
    return jsonify({
      "message": "You are not authorized to make this action"
    }), 401

@roles.route('/api/v1/roles/update/<int:id>', methods=['PUT'])
def RoleUpdate(id):
  bearer = request.headers.get('Authorization')
  auth = JWTAuth(bearer).decode()
  if auth and auth["role"] <= 3:
    data = request.get_json()
    slug = Functions().strToSlug(data["role_name"])
    data["role_slug"] = slug
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