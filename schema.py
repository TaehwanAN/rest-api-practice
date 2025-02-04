from marshmallow import Schema, fields

# plain schema: without relational fields
# schema: with all fields
class UserSchema(Schema):
  id = fields.Int(dump_only=True) # dump_only: read_only, only in response, serialization
  userid = fields.Str(required=True)
  password = fields.Str(required=True, load_only=True) # write_only, only in request, deserialization
  username = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  is_active = fields.Boolean(dump_only=True)
  is_delete = fields.Boolean(dump_only=True)
