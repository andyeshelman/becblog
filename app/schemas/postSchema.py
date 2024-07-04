from app.schemas import ma
from marshmallow import fields

class PostSchema(ma.Schema):
    id = fields.Integer(required=False)
    user_id = fields.Integer(required=True)
    title = fields.String(required=True)
    body = fields.String(required=True)

post_schema = PostSchema()
post_schema_edit = PostSchema(only=['title', 'body'])
posts_schema = PostSchema(many=True)