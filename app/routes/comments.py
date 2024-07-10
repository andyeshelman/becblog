from flask import request

from app import app
from app.modules import db, token_auth, cache,limiter
from app.models import Comment
from app.schemas.commentSchema import comment_schema, comment_schema_body, comments_schema
from app.utils.exc import handler, NotFound, ContentType, Permission

@app.get('/comments')
@token_auth.login_required
@cache.cached(timeout=60, query_string=True)
@limiter.limit('100 per day')
def get_all_comments():
    query = db.select(Comment)
    comments = db.paginate(query)
    return comments_schema.jsonify(comments)

@app.get('/comments/<int:comment_id>')
@token_auth.login_required
@cache.cached(timeout=60)
@limiter.limit('100 per day')
@handler
def get_one_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if comment is None:
        raise NotFound(f"comment with ID {comment_id}")
    return comment_schema.jsonify(comment)

@app.put('/comments/<int:comment_id>')
@token_auth.login_required
@limiter.limit('100 per day')
@handler
def put_comment(comment_id):
    if not request.is_json:
        raise ContentType("application/json")
    comment = db.session.get(Comment, comment_id)
    if comment is None:
        raise NotFound(f"comment with ID {comment_id}")
    user = token_auth.current_user()
    if not user is comment.user:
        raise Permission("edit this comment")
    diff_data = comment_schema_body.load(request.json, partial=True)
    for key, value in diff_data.items():
        setattr(comment, key, value)
    db.session.commit()
    return comment_schema.jsonify(comment)