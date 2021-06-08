from marshmallow import Schema, fields
from marshmallow.fields import String


# Validation Schemas #######################
class LoginSchema(Schema):
    username: String = fields.Str(required=True)
    password: String = fields.Str(required=True)
