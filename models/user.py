from db import db
from datetime import datetime
from passlib.hash import pbkdf2_sha256 # user password encryption

# create model
class UserModel(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key = True)
  userid = db.Column(db.String(80), unique=True, nullable = False)
  password = db.Column(db.String(256), nullable= False)
  username = db.Column(db.String(40), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now())
  is_active = db.Column(db.Boolean, default=True)
  is_delete = db.Column(db.Boolean, default=False)
  is_admin = db.Column(db.Boolean, default=False)

  def __repr__(self):
    return f"User ID: {self.userid}, User Name: {self.username}, Joined: {self.created_at.strftime('%Y-%m-%d')}"
  
  def set_password(self, password):
    self.password = pbkdf2_sha256.hash(password)
  
  def check_password(self, password):
    return pbkdf2_sha256.verify(password, self.password)
  