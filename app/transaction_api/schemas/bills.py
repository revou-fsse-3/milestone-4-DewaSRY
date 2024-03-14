from marshmallow import Schema , fields,post_load

from app.transaction_api.model.bills import BillsModel

class BillUpdateSchemas(Schema):
    biller_name=fields.Str()
    amount=fields.Float()
    date_line_days=fields.Integer()

class BillBaseSchemas(BillUpdateSchemas):
    account_id=fields.Str()
    
class BillCreateSchemas(BillBaseSchemas):
    user_id=fields.Str()
    
    @post_load
    def create_Bill(self, data, **kwargs):
        return BillsModel(**data)
        
class BillResponseSchemas(BillCreateSchemas):
    id=fields.Str()
    due_date = fields.DateTime()