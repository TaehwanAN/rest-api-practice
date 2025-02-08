from sqlalchemy import func
from db import db

class PurchaseModel(db.Model):
  __tablename__="purchases"

  purchase_id = db.Column(db.Integer, primary_key=True)
  customer_id = db.Column(db.String(36), db.ForeignKey("customers.customer_id"), unique = False, nullable=False)
  product_id = db.Column(db.String(36), db.ForeignKey("products.product_id"), unique = False, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  datetime = db.Column(db.DateTime, default = func.now()) # dynamic default # DateTime(o), Datetime(x)

  customer = db.relationship("CustomerModel", back_populates="purchases")
  product = db.relationship("ProductModel", back_populates = "purchases")

  def __str__(self):
    return f"Purchase Info: {self.customer_id.company_name} purchased {self.product_id.product_name} x {self.quantity} at {self.datetime.strftime('%Y-%m-%d')}"