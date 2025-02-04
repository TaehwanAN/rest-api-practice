from flask.views import MethodView
from flask_smorest import Blueprint, abort
from psycopg2 import IntegrityError

from schema import UserSchema

from db import db
from models.user import UserModel


from passlib.hash import pbkdf2_sha256 # user password encryption

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
        password = pbkdf2_sha256.hash(user_data.get("password")),
        username= user_data.get("username")
      )
      # db transaction
      db.session.add(user)
      db.session.commit()
      # return message
      return {
        "message": f"Welcome {user.username}(ID: {user.userid})."
      }
    except IntegrityError as e:
      abort(
        409, message=str(e.__str__)
      )
    