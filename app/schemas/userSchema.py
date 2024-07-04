from app.schemas import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    email = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)

user_schema = UserSchema()
user_schema_nopass = UserSchema(exclude=['password'])
user_schema_login = UserSchema(only=['username', 'password'])
user_schema_edit = UserSchema(exclude=['id'])
users_schema = UserSchema(many=True, exclude=['password'])