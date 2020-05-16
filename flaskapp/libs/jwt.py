import jwt
import time
from flaskapp import app

class JWTAuth:
  def __init__(self, payload, id):
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
      "role": ""
    }
    self.algorithm = 'RS256'

  def encode(self):
    # Load the key we created
    # TODO: REVISAR PORQUE EN https://jwt.io/ DA EL ERROR DE INVALID SIGNATURE
    private = open("flaskapp/keys/flaskapp").read()
    return jwt.encode(self.message, private, algorithm=self.algorithm).decode()
  
  def decode(self, jwtString):
    # Load the public key to run another test...
    with open("flaskapp/keys/flaskapp.pub", "rb") as key_file:
      public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())
      return jwt.decode(jwtString, public_key, algorithms=self.algorithm)