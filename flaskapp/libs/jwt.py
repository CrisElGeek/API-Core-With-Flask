import jwt
import time
from flaskapp import app

class JWTAuth:
  def __init__(self, payload, id = False):
    if not id:
      self.bearer = payload
    else:
      self.message = {
        "iss": app.config["JWT_ISS"],
        "exp": int(time.time()) + app.config["JWT_MAX_LIFETIME"],
        "website": app.config["JWT_WEBSITE"],
        "iat": int(time.time()),
        "client_id": id,
        "email": payload["email"][0],
        "auth_time": int(time.time()),
        "given_name": payload["first_name"][0],
        "family_name": payload["last_name"][0],
        "jti": app.config["JWT_JTI"],
        "sub": "everyone",
        "role": payload["role_id"][0]
      }
    self.algorithm = 'RS256'

  def encode(self):
    # Load the key we created
    private = open("flaskapp/keys/id_rsa").read()
    return jwt.encode(self.message, private, algorithm=self.algorithm).decode('utf-8')
  
  def decode(self):
    # Load the public key to run another test...
    with open("flaskapp/keys/id_rsa.pub", "rb") as key_file:
      public_key = open("flaskapp/keys/id_rsa.pub").read()
      result = None
      try:
        result = jwt.decode(self.bearer, public_key, algorithms=self.algorithm)
      except:
        result = None
      return result