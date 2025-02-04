# local 실행: flask run --port 15000

# environment setting
import os 
from dotenv import load_dotenv

from flask import Flask # app run
from flask_smorest import Api # api register

from db import db # database SQLAlchemy
from flask_migrate import Migrate # database migration

from resources.user import blp as UserBluePrint # resource registration

def create_app(prd=False): # Factory pattern
  app = Flask(__name__) # app object create
  load_dotenv() # load .env
  # debug
  app.config["PROPAGATE_EXCEPTIONS"] = True
  # api setting
  app.config["API_TITLE"] = "Taehwan REST API"
  app.config["API_VERSION"] = "v1"
  # api documentation
  app.config["OPENAPI_VERSION"] = "3.0.3"
  app.config["OPENAPI_URL_PREFIX"] = "/"
  app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
  app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  # database url setting(docker cmd -> create_app(prd=True))
  if prd:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL_PRD")
  else:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL_DEV")
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  # Flask-SQLAlchemy 초기화
  db.init_app(app)
  migrate = Migrate(app, db)
  # Flask-Smorest API 초기화
  api = Api(app)

  api.register_blueprint(UserBluePrint)

  return app
