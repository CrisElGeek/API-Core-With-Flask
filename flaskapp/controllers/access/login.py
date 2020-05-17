from flask import jsonify, Blueprint, request
from flaskapp.models.middleware import Models
from flaskapp.libs.form_validation import Validate
from argon2 import PasswordHasher
from flaskapp.libs.jwt import JWTAuth
import sys

access = Blueprint('access', __name__)

get_params = {
  "database": "users u",
  "fields": {
    "id": {"field": "u.id", "protected": True},
    "first_name": {"field": "u.first_name"},
    "last_name": {"field": "u.last_name"},
    "email": {"field": "u.email"},
    "phone": {"field": "u.phone"},
    "status_id": {"field": "u.status_id"},
    "password": {"field": "u.password"},
    "role_id": {"field": "u.role_id"},
    "permissions": {"field": "u.permissions"}
  },
  "filters": []
}

rules = {
  "email": "required|max:150|email",
  "password": "required|min:6"
}

@access.route('/api/v1/access/login', methods=['POST'])
def login():
  data = request.get_json()
  get_params["filters"] = [{
    "field": "email",
    "value": data["email"],
    "operator": "="
  }]
  results = Models(get_params, data)
  payload = results.Params()
  errors = Validate().execute(payload, rules)
  if len(errors) == 0:
    res = results.Get()
    if res["code"] == 200:
      ph = PasswordHasher()
      try:
        ph.verify(res["data"][0]["password"], data["password"])
      except:
        return jsonify({
          "message": "Invalid email and/or password",
          "code": 401
        }), 401
        sys.exit()
      userInfo = {
        "first_name": [res["data"][0]["first_name"]],
        "last_name": [res["data"][0]["last_name"]],
        "role_id": [res["data"][0]["role_id"]],
        "email": [res["data"][0]["email"]]
      }
      auth = JWTAuth(userInfo, res["data"][0]["id"]).encode()
      return jsonify({
        "bearer": auth,
        "message": "Successfully logged In"
        }), res["code"]
    else:
      return jsonify(res), res["code"]
  else:
    return jsonify(errors), 400
