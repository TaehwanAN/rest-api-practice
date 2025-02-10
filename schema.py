from marshmallow import Schema, fields

# plain schema: without relational fields
# schema: with all fields
class PlainUserSchema(Schema): # register
  id = fields.Int(dump_only=True) # dump_only: read_only, only in response, serialization
  userid = fields.Str(required=True)
  password = fields.Str(required=True, load_only=True) # write_only, only in request, deserialization
  username = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  is_active = fields.Boolean(dump_only=True)
  is_delete = fields.Boolean(dump_only=True)
  is_admin = fields.Boolean(dump_only=True)

class LoginUserSchema(PlainUserSchema): # login
  username = fields.Str() # To login, only userid and password required

class PlainCustomerSchema(Schema): # post
  customer_id = fields.Str(dump_only=True)
  company_name = fields.Str(required=True)

class PlainProductSchema(Schema): # post 
  product_id = fields.Str(dump_only=True)
  product_name = fields.Str(required=True)
  unit_price = fields.Float(required=True)

class PlainPurchaseSchema(Schema): # post
  purchase_id = fields.Int(dump_only = True)
  customer_id = fields.Str(load_only = True)
  customer = fields.Nested(PlainCustomerSchema(), dump_only=True)
  product_id = fields.Str(load_only=True)
  product = fields.Nested(PlainProductSchema(), dump_only=True)
  quantity = fields.Int(required=True)
  datetime = fields.DateTime(dump_only=True)
  is_deleted = fields.Boolean(dump_only=True)

class DetailCustomerSchema(PlainCustomerSchema): # put
  company_name = fields.Str(required=False)
  is_deleted = fields.Boolean(dump_only=True)
  purchases = fields.List(fields.Nested(PlainPurchaseSchema()), dump_only=True)
  
class DetailProductSchema(PlainProductSchema): # put
  product_name = fields.Str(required=False)
  unit_price = fields.Float(required=False)
  is_deleted = fields.Boolean(dump_only=True)
  purchases = fields.List(fields.Nested(PlainPurchaseSchema()), dump_only=True)
