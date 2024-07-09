from app.schemas import ma
from marshmallow import fields

class CommentSchema(ma.Schema):
    id = fields.Integer(required=False)
    user_id = fields.Integer(required=True)
    post_id = fields.Integer(required=True)
    body = fields.String()

comment_schema = CommentSchema()
comment_schema_body = CommentSchema(only=['body'])
comments_schema = CommentSchema(many=True)