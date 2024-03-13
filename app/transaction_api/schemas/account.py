from marshmallow import Schema, fields,post_load
from app.transaction_api.model.account import AccountModel


class AccountBaseSchemas(Schema):
    """base account schemas for update"""
    account_type=fields.Str()
    account_number=fields.Str()
    balance=fields.Float()


class AccountPayloadSchemas(AccountBaseSchemas):
    """account Create Account"""
    user_id=fields.Str() 
    
class AccountCreateSchemas(AccountPayloadSchemas):
    """schemas for create account"""
    @post_load
    def create_account(self, data, **kwargs):
        return AccountModel(**data)


class AccountResponseSchema(AccountPayloadSchemas):
    """schemas response account after create account"""
    id=fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    
