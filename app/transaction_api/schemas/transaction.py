from marshmallow import Schema, fields,post_load
from app.transaction_api.model.transaction import TransactionsModel
from app.transaction_api.model.account import AccountModel


from app.transaction_api.util.db import db


class TransactionPayloadSchemas(Schema):
    """base transaction payload to create Transaction"""
    from_account_id=fields.Str(required=True)
    to_account_id=fields.Str(required=True)
    amount = fields.Float(required=True)
    type=fields.Str(required=False)
    description=fields.Str(required=False)
    

class TransactionCreateSchemas(TransactionPayloadSchemas):
    """Transaction to load Transaction model"""
    @post_load
    def create_Transactions(self, data, **kwargs):
        from_account_id=data['from_account_id']
        to_account_id=data['to_account_id']
        amount = data['amount']
        accountFrom:AccountModel= AccountModel.query.get_or_404(from_account_id)
        try:  
            accountFrom.transfer(amount, to_account_id )
        except ValueError as e:
            raise e
        db.session.commit()
        try: 
          return TransactionsModel(**data)
        except ValueError as e:
            raise e

class TransactionsResponseSchema(TransactionPayloadSchemas):
    """Transaction response """
    id=fields.Str()
    created_at = fields.DateTime()
    
    
class TransactionCategoryListSchemas(Schema):
    name=fields.Str()
    transaction=fields.List(fields.Nested(TransactionsResponseSchema()), dump_only=True)