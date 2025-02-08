from flask_smorest import Blueprint, abort
from flask.views import MethodView

from db import db
from models.shop.transaction_data import PurchaseModel
from schema import PlainPurchaseSchema

purchase_blp = Blueprint("Purchase", "purchases", description="Operations on purchases")

@purchase_blp.route("/purchases")
class Purchases(MethodView):

  @purchase_blp.arguments(PlainPurchaseSchema)
  @purchase_blp.response(200,PlainPurchaseSchema)
  def post(self,purchase_data):
    purchase = PurchaseModel(**purchase_data)

    try:
      db.session.add(purchase)
      db.session.commit()
    except Exception as e:
      abort(400,exc=e)
    
    return purchase
  
  @purchase_blp.response(200,PlainPurchaseSchema(many=True))
  def get(self):
    return PurchaseModel.query.all()
  
@purchase_blp.route("/purchases/<int:purchase_id>")
class Purchase(MethodView):

  @purchase_blp.response(200, PlainPurchaseSchema)
  def get(self,purchase_id):
    purchase = PurchaseModel.query.get_or_404(purchase_id)
    if not purchase or purchase.is_deleted:
      abort(409, message="not exsiting purchase")
    return purchase

  @purchase_blp.arguments(PlainPurchaseSchema)
  @purchase_blp.response(200, PlainPurchaseSchema)
  def put(self,purchase_data, purchase_id ): # update only # insert=post # included patch (mynote.txt->post,put,patch 차이이)
    purchase = PurchaseModel.query.get_or_404(purchase_id)
    if not purchase or purchase.is_deleted:
      abort(409, message="not exsiting purchase")
    for key, value in purchase_data.items(): # blp arguments를 통해 속성 유효값을 검증하기 때문에 사용 가능. 검증 없으면 잘못된 속성으로 인한 DB 단에서 에러 발생 가능함.
      setattr(purchase,key,value)
    db.session.commit()
    return purchase

  def delete(self,purchase_id):
    purchase = PurchaseModel.query.get_or_404(purchase_id)

    # db.session.delete(customer)
    # db.session.commit()

    if not purchase or purchase.is_deleted:
      abort(409, message="not exsiting purchase")
    
    purchase.is_deleted = True
    db.session.commit()
    return {"message": f"Deleted: {purchase}"}
  
@purchase_blp.route("/purchases/customers/<string:customer_id>/products/<string:product_id>")
class SpecificPurchases(MethodView):

  @purchase_blp.response(200,PlainPurchaseSchema(many=True))
  def get(self,customer_id,product_id):
    purchases = PurchaseModel.query.filter_by(customer_id=customer_id,product_id=product_id)

    if not purchases:
      abort(409, message="not exsiting purchase")
    
    return purchases