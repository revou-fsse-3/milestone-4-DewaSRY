from marshmallow import Schema, fields


class UserBase(Schema):
    
    username= fields.Str()
    email= fields.Str()
    password= fields.Str()
    
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    