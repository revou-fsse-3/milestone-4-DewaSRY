from marshmallow import Schema, fields,post_load
from app.transaction_api.model.account import AccountModel


class AccountUpdateSchemas():
    account_type=fields.Str()
    account_number=fields.Str()
    balance=fields.Float()


class AccountBaseSchemas(AccountUpdateSchemas):
    user_id=fields.Str() 
    # @post_load
    def create_account(self, data, **kwargs):
        return AccountModel(**data)


class AccountResponseSchema(AccountBaseSchemas):
    id=fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    
