from marshmallow import Schema, fields, validate, ValidationError

class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class PostSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    content = fields.Str(required=True)
