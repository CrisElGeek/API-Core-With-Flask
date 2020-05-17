from flask import jsonify, Blueprint, request
from flaskapp.models.middleware import Models
from flaskapp.libs.form_validation import Validate
from argon2 import PasswordHasher
import sys

access = Blueprint('access', __name__)

get_params = {
  "database": "users u",
  "fields": {
    "email": {"field": "u.email"},
    "password": {"field": "u.password"}
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
      return jsonify({
        "message": "Login Correct",
        "code": 201 
      }), 201
    else:
      return jsonify(res), res["code"]
  else:
    return jsonify(errors), 400
