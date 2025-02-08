from db import db

class CustomerModel(db.Model):
  __tablename__ = "customers"

  customer_id = db.Column(db.String(36), primary_key = True) # uuid4
  company_name = db.Column(db.String(100), nullable=False) # db.String: char varying / db.Char: char
  is_deleted = db.Column(db.Boolean(), default=False)

  purchases = db.relationship("PurchaseModel", back_populates = "customer", lazy="dynamic", cascade="all, delete")

  def __repr__(self):
    return f"<Customer: {self.company_name}({self.customer_id})>"
  
  @classmethod
  def get_active_or_404(cls, customer_id):
      """삭제되지 않은 고객을 가져오거나 404 반환"""
      return cls.query.filter_by(customer_id=customer_id, is_deleted=False).first_or_404(
          description="Customer not found or deleted"
      )

class ProductModel(db.Model):
  __tablename__ = "products"

  product_id = db.Column(db.String(36), primary_key = True)
  product_name = db.Column(db.String(255), nullable=False)
  unit_price = db.Column(db.Float(precision=2), nullable=False)
  is_deleted = db.Column(db.Boolean(), default=False)

  purchases = db.relationship("PurchaseModel", back_populates = "product", lazy="dynamic", cascade="all, delete")
  
  def __repr__(self):
    return f"Product: {self.product_name}({self.product_id})"
  
  @classmethod
  def get_active_or_404(cls, product_id):
      """삭제되지 않은 상품품을 가져오거나 404 반환"""
      return cls.query.filter_by(product_id=product_id, is_deleted=False).first_or_404(
          description="Product not found or deleted"
      )
