from marshmallow import Schema, fields


# Validation Schemas #######################
class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
