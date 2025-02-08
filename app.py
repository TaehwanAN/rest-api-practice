# local 실행: flask run --port 15000

# environment setting
import os 

from flask import Flask # app run
from flask_jwt_extended import JWTManager
from flask_smorest import Api # api register

from db import db, BLOCKLIST # database SQLAlchemy
from flask_migrate import Migrate # database migration

from resources.conn_test import blp as ConnTestBluePrint
from resources.user import blp as UserBluePrint # resource registration
from resources.shop.master_data import customer_blp as CustomerBluePrint, product_blp as ProductBluePrint

def create_app(): # Factory pattern
  app = Flask(__name__) # app object create
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
  database_url = os.environ.get("DATABASE_URL")
  app.config["SQLALCHEMY_DATABASE_URI"] = database_url
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  # Flask-SQLAlchemy 초기화
  db.init_app(app)
  migrate = Migrate(app, db)
  # JWT Setting
  app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
  jwt=JWTManager(app)
  ## for logout using jwt(jti) blocklist
  @jwt.token_in_blocklist_loader
  def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST
  # Flask-Smorest API 초기화
  api = Api(app)
  api.register_blueprint(UserBluePrint)
  api.register_blueprint(ConnTestBluePrint)
  api.register_blueprint(CustomerBluePrint)
  api.register_blueprint(ProductBluePrint)

  return app
