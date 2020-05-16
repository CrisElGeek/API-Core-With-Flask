# Statement for enabling the development environment
DEBUG = True
# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
# Define the database - we are working with
# SQLite for this example
MYSQL_HOST = "localhost"
MYSQL_USER = "criselgeek"
MYSQL_PASSWORD =  "criselgeek1"
MYSQL_DB = "flaskx"
MYSQL_PORT = 3306
MYSQL_CHARSET = "utf8mb4"
MYSQL_CURSORCLASS = "DictCursor"
# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_ENABLED = True
CSRF_SESSION_KEY = "secret"
# Secret key for signing cookies
JWT_ISS = "https://criselgeek.com"
JWT_WEBSITE = "http://cris.com.mx"
JWT_MAX_LIFETIME = 86400
JWT_JTI = "CrisElGeek80FlaskTest"