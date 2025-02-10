from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort
from psycopg2 import IntegrityError

from schema import LoginUserSchema, PlainUserSchema

from db import db, BLOCKLIST
from models.user import UserModel

# create blueprint object for API documentation
blp = Blueprint("Users","users", description="Operations on users")

# set route -> URL/user/register
@blp.route("/user/register")
class UserRegister(MethodView):

  # validation, schema transformation, parsing
  @blp.arguments(PlainUserSchema)
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

@blp.route("/users/<int:user_id>")
class Users(MethodView):

  @blp.response(200,LoginUserSchema)
  def get(self, user_id):
    user = UserModel.query.get_or_404(user_id)
    return user
  
  @jwt_required
  def delete(self, user_id):
    user = UserModel.query.get_or_404(user_id)
    

@blp.route("/user/login")
class UserLogin(MethodView):

  @blp.arguments(LoginUserSchema)
  def post(self, user_data):
    user = UserModel.query.filter(
      UserModel.userid == user_data.get("userid")
    ).first()

    if not user:
      return {"message":"User ID Not Found"}
    if not user.check_password(user_data.get("password")):
      return {"message":"Wrong Password"}
    
    access_token = create_access_token(identity=str(user.id), fresh = True) # jwt.io(웹) # client must include {"Authorization": "Bearer access_token"} in Headers
    refresh_token = create_refresh_token(identity = str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token}

@blp.route("/user/logout")
class UserLogout(MethodView):

  @jwt_required()
  def post(self):
    jti = get_jwt().get("jti") # jwt unique id
    BLOCKLIST.add(jti)
    return {"message":"Successfully Logged Out"}
  
@blp.route("/refresh")
class TokenRefresh(MethodView):

  @jwt_required(refresh=True)
  def post(self):
    """
    Keyword arguments:
    argument -- refresh_token
    Return: access_token
    """
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False) # fresh = false -> 최초로 발급된 토큰 아니라는 뜻
    jti = get_jwt().get("jti") # 기존 access token은 폐기한다
    BLOCKLIST.add(jti)
    return {"access_token": new_token}