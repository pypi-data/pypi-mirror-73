from marshmallow import Schema, fields

class IndexSchema(Schema):
  id = fields.Int(required=True)
  index_name = fields.Str()
  index_acr = fields.Str()
  country = fields.Str()

class StockSchema(Schema):
  id = fields.Int(required=True)
  symbol = fields.Str()
  name = fields.Str()
  index = fields.Int(required=True)

class StockPriceSchema(Schema):
  id = fields.Int(required=True)
  symbol = fields.Str()
  date = fields.Date()
  open = fields.Decimal()
  high = fields.Decimal()
  low = fields.Decimal()
  close = fields.Decimal()
  last = fields.Decimal()
  prev_close = fields.Decimal()
  volume = fields.Number()
  index = fields.Int(required=True)