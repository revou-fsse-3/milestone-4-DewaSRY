from marshmallow import Schema, fields,post_load
from app.transaction_api.model.transaction import TransactionsModel
from app.transaction_api.model.account import AccountModel
from app.transaction_api.service.ModelMatcher import matherAccountModeWIthId


from app.transaction_api.util.db import db


class TransactionsBaseSchemas(Schema):
    from_account_id=fields.Str(required=True)
    to_account_id=fields.Str(required=True)
    amount = fields.Float(required=True)
    type=fields.Str(required=False)
    description=fields.Str(required=False)
    
    # @post_load
    @classmethod
    def create_Transactions(self, data, **kwargs):
        from_account_id=data['from_account_id']
        to_account_id=data['to_account_id']
        amount = data['amount']
        # type=data['type']
        # description=data['description']
        
        accountFrom:AccountModel= matherAccountModeWIthId(from_account_id)
        accountTo:AccountModel=matherAccountModeWIthId(to_account_id)
        if accountFrom.balance < amount:
            raise ValueError(f"acount with id : {from_account_id} have not enough money")
        accountFrom.update(balance=accountFrom.balance- amount )
        accountTo.update(balance=accountTo.balance+ amount )
        db.session.add_all([accountFrom,accountTo ])
        db.session.commit()
        return TransactionsModel(**data)






class TransactionsResponseSchema(TransactionsBaseSchemas):
    id=fields.Str()
    created_at = fields.DateTime()
    
    
