from marshmallow import Schema, fields,post_load

from app.transaction_api.model.user import UserModel
class UserBaseSchema(Schema):
    username= fields.Str()
    email= fields.Str()
    password= fields.Str()
    

    @post_load
    def create(self, data, **kwargs):
        return UserModel(**data)

class UseResponseSchema(UserBaseSchema):
    id=fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()