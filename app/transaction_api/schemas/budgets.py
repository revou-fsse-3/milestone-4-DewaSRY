from marshmallow import Schema , fields,post_load

from app.transaction_api.model.budgets import BudgetsModel

class BudgetBaseSchemas(Schema):
    name=fields.Str()
    amount=fields.Float()
    date_line_days=fields.Integer()
    
class BudgetCreateSchemas(BudgetBaseSchemas):
    user_id=fields.Str()
    
    @post_load
    def create_budget(self, data, **kwargs):
        return BudgetsModel(**data)
        
class BudgetResponseSchemas(BudgetCreateSchemas):
    id=fields.Str()
    start_date = fields.DateTime()
    end_date = fields.DateTime()