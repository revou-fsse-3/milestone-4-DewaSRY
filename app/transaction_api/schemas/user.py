from marshmallow import Schema, fields,post_load

from app.transaction_api.model.user import UserModel

class UserPayloadSchema(Schema):
    """payload to create schemas"""
    username= fields.Str()
    email= fields.Str()
    password= fields.Str()
    
class UserCreateSchema(UserPayloadSchema):
    """schemas to create Model"""
    @post_load
    def create(self, data, **kwargs):
        return UserModel(**data)

class UseResponseSchema(UserPayloadSchema):
    """schemas to response user schemas"""
    id=fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()