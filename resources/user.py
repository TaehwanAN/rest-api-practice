from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from psycopg2 import IntegrityError

from schema import UserLoginSchema, UserSchema

from db import db, BLOCKLIST
from models.user import UserModel

# create blueprint object for API documentation
blp = Blueprint("Users","users", description="Operations on users")

# set route -> URL/user/register
@blp.route("/user/register")
class UserRegister(MethodView):

  # validation, schema transformation, parsing
  @blp.arguments(UserSchema)
  def post(self,user_data):
    try:
      # create UserModel object
      user = UserModel(
        userid = user_data.get("userid"),
        username= user_data.get("username")
      )
      user.set_password(user_data.get("password"))
      # db transaction
      db.session.add(user)
      db.session.commit()
      # return message
      return {
        "message": f"Welcome {user.username}!!(ID: {user.userid})."
      }
    except IntegrityError as e:
      abort(
        409, message="User ID Already Exists" ,error=str(e.__str__)
      )

@blp.route("/user/login")
class UserLogin(MethodView):

  @blp.arguments(UserLoginSchema)
  def post(self, user_data):
    user = UserModel.query.filter(
      UserModel.userid == user_data.get("userid")
    ).first()

    if not user:
      return {"message":"User ID Not Found"}
    if not user.check_password(user_data.get("password")):
      return {"message":"Wrong Password"}
    
    access_token = create_access_token(identity=str(user.id)) # jwt.io(웹) # client must include {"Authorization": "Bearer access_token"} in Headers
    return {"access_token": access_token}

@blp.route("/user/logout")
class UserLogout(MethodView):

  @jwt_required()
  def post(self):
    jti = get_jwt().get("jti") # jwt unique id
    BLOCKLIST.add(jti)
    return {"message":"Successfully Logged Out"}