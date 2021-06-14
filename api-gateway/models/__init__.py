from marshmallow import Schema, fields
from marshmallow.fields import String, Email


# Validation Schemas #######################
class UserSchema(Schema):
    full_name: String = fields.Str(required=True)
    email: Email = fields.Email(required=True)
    organization: String = fields.Str(required=True)
    profession: String = fields.Str(required=True)
    reason: String = fields.Str(required=True)
    password: String = fields.Str(required=True)
