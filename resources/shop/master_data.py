import uuid

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from psycopg2 import IntegrityError

from db import db
from models.shop.master_data import CustomerModel, ProductModel
from schema import DetailCustomerSchema, DetailProductSchema, PlainCustomerSchema, PlainProductSchema
from utils import get_random_code

customer_blp = Blueprint("Customer", "Customers", description = "operations on customers")
product_blp = Blueprint("Product","Products", description = "operations on products")

@customer_blp.route("/customers")
class Customers(MethodView):

  @customer_blp.arguments(PlainCustomerSchema)
  @customer_blp.response(200, PlainCustomerSchema)
  def post(self, customer_data):
    # transformation for constraints
    customer_data["customer_id"] = str(uuid.uuid4())
    # customer_data["company_name"]+=get_random_code()

    customer = CustomerModel(**customer_data)
    
    try:
      db.session.add(customer)
      db.session.commit()
    except IntegrityError:
      abort(400, message="already exists")
    return customer
  
  @customer_blp.response(200, PlainCustomerSchema(many=True))
  def get(self):
    return CustomerModel.query.all()
  
@customer_blp.route("/customers/<string:customer_id>") # parameter customer_id should be positioned at last
class Customer(MethodView):
  
  @customer_blp.response(200, DetailCustomerSchema)
  def get(self,customer_id):
    customer = CustomerModel.get_active_or_404(customer_id)
    return customer

  @customer_blp.arguments(DetailCustomerSchema)
  @customer_blp.response(200, DetailCustomerSchema)
  def put(self,customer_data, customer_id ): # update only # insert=post # included patch (mynote.txt->post,put,patch 차이이)
    customer = CustomerModel.get_active_or_404(customer_id)
    if not customer:
      abort(409, message="not exsiting customer")
    
    for key, value in customer_data.items(): # blp arguments를 통해 속성 유효값을 검증하기 때문에 사용 가능. 검증 없으면 잘못된 속성으로 인한 DB 단에서 에러 발생 가능함.
      setattr(customer,key,value)
    db.session.commit()
    return customer

  def delete(self,customer_id):
    customer = CustomerModel.query.get(customer_id)

    # db.session.delete(customer)
    # db.session.commit()

    if not customer:
      abort(409, message="not exsiting customer")
    
    customer.is_deleted = True
    db.session.commit()
    return {"message": f"{customer.company_name} deleted"}
  

@product_blp.route("/products")
class Products(MethodView):

  @product_blp.arguments(PlainProductSchema)
  @product_blp.response(200, PlainProductSchema)
  def post(self, product_data):
    # transformation for constraints
    product_data["product_id"] = str(uuid.uuid4())

    product = ProductModel(**product_data)
    
    try:
      db.session.add(product)
      db.session.commit()
    except IntegrityError:
      abort(400, message="already exists")
    return product
  
  @product_blp.response(200, PlainProductSchema(many=True))
  def get(self):
    return ProductModel.query.all()
  
@product_blp.route("/products/<string:product_id>") # parameter product_id should be positioned at last
class Product(MethodView):
  
  @product_blp.response(200, DetailProductSchema)
  def get(self,product_id):
    product = ProductModel.get_active_or_404(product_id)
    return product

  @product_blp.arguments(DetailProductSchema)
  @product_blp.response(200, DetailProductSchema)
  def put(self,product_data, product_id ): # update only # insert=post # included patch (mynote.txt->post,put,patch 차이이)
    product = ProductModel.get_active_or_404(product_id)
    if not product:
      abort(409, message="not exsiting product")
    
    for key, value in product_data.items(): # blp arguments를 통해 속성 유효값을 검증하기 때문에 사용 가능. 검증 없으면 잘못된 속성으로 인한 DB 단에서 에러 발생 가능함.
      setattr(product,key,value)
    db.session.commit()
    return product

  def delete(self,product_id):
    product = ProductModel.query.get(product_id)

    # db.session.delete(product)
    # db.session.commit()

    if not product:
      abort(409, message="not exsiting product")
    
    product.is_deleted = True
    db.session.commit()
    return {"message": f"{product.product_name} deleted"}