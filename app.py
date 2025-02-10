# local 실행: flask run --port 15000

# environment setting
import os 

from flask import Flask, jsonify # app run
from flask_jwt_extended import JWTManager
from flask_smorest import Api # api register

from db import db, BLOCKLIST # database SQLAlchemy
from flask_migrate import Migrate # database migration

from resources.conn_test import blp as ConnTestBluePrint
from resources.user import blp as UserBluePrint # resource registration
from resources.shop.master_data import customer_blp as CustomerBluePrint, product_blp as ProductBluePrint
from resources.shop.transaction_data import purchase_blp as PurchaseBluePrint

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
  # jwt blocklist
  @jwt.token_in_blocklist_loader
  def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

  # revoked(BLOCKLIST 된)
  @jwt.revoked_token_loader
  def revoked_token_callback(jwt_header, jwt_payload):
    return (
      jsonify(
        {"description": "The token has been revoked", "error":"token_revoked"}
      ), 401
    )

  # refresh
  @jwt.needs_fresh_token_loader
  def token_not_fresh_callback(jew_header,jwt_payload):
    return (
      jsonify(
        {"description": "The token is not fresh", "error": "fresh_token_required"}
      ), 401
    )

  # jwt claims
  @jwt.additional_claims_loader
  def add_claims_to_jwt(identity): # create_accsee_token -> identity
    # actually: need to look up user propertiy
    if identity == "1": # identity => user.id
      return {
        "is_admin": True
      }
    else:
      return {"is_admin": False}

  # jwt 커스터마이징 -> 이미 JWTManger에 있는 메소드
  # 콜백은 다른 함수가 실행된 후 호출되는 함수를 의미합니다.
  # 즉, 어떤 동작이 끝난 뒤 실행되도록 미리 등록하는 함수입니다.
  @jwt.expired_token_loader
  def expired_token_callback(jwt_header, jwt_payload):
    return (
      jsonify(
        {
          "message": "The token has expired.",
          "error" : "token_expired"
        }
      ), 401
    )

  @jwt.invalid_token_loader
  def invalid_token_callback(error):
    return (
      jsonify(
        {
          "message": "Signature verification failed",
          "error": "invalid_token"
        }
      ), 401
    )

  @jwt.unauthorized_loader
  def missing_token_callback(error):
    return (
      jsonify(
        {
          "message": "Request does not conatin an access token",
          "error": "authroization_required"
        }
      ), 401
  )
  # Flask-Smorest API 초기화
  api = Api(app)
  api.register_blueprint(UserBluePrint)
  api.register_blueprint(ConnTestBluePrint)
  api.register_blueprint(CustomerBluePrint)
  api.register_blueprint(ProductBluePrint)
  api.register_blueprint(PurchaseBluePrint)

  return app
