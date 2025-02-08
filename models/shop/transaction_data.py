from sqlalchemy import func
from db import db
from models.shop.master_data import CustomerModel, ProductModel

class PurchaseModel(db.Model):
  __tablename__="purchases"

  purchase_id = db.Column(db.Integer, primary_key=True)
  customer_id = db.Column(db.String(36), db.ForeignKey("customers.customer_id"), unique = False, nullable=False)
  product_id = db.Column(db.String(36), db.ForeignKey("products.product_id"), unique = False, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  datetime = db.Column(db.DateTime, default = func.now()) # dynamic default # DateTime(o), Datetime(x)
  is_deleted = db.Column(db.Boolean, default = False)

  customer = db.relationship("CustomerModel", back_populates="purchases")
  product = db.relationship("ProductModel", back_populates = "purchases")

  def __str__(self):
    company_name = CustomerModel.query.get(self.customer_id)
    product_name = ProductModel.query.get(self.product_id)
    return f"Purchase Info: {company_name} purchased {product_name}(Quantity: {self.quantity}, Date:{self.datetime.strftime('%Y-%m-%d')})"
  
