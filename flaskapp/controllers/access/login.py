from flask import jsonify, Blueprint, request
from flaskapp.models.middleware import Models
from flaskapp.libs.form_validation import Validate
from argon2 import PasswordHasher

access = Blueprint('access', __name__)

get_params = {
  "database": "users u",
  "fields": {
    "email": {"field": "u.email"},
    "password": {"field": "u.password"}
  }
}

rules = {
  "email": "required|max:150|email",
  "password": "required|min:6"
}

@access.route('/api/v1/acces/login', methods=['POST'])
def login():
  data = request.get_json()
  results = Models(get_params, data)
  payload = results.Params()
  errors = Validate().execute(payload, rules)
  if len(errors) == 0:
    res = results.Get()
    if res["code"] == 200:
      ph = PasswordHasher()
      validEmail = ph.verify(res["password"], data["password"][0])
      if validEmail:
        #
      else:
        return jsonify({
          "message": "Invalid email and/or password",
          "code": 401
        }), 401
    else:
      return jsonify(res), res["code"]
  else:
    return jsonify(errors), 400
