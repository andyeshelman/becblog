from flask import request

from app import app
from app.modules import db, token_auth, cache, limiter
from app.models import Role, User, Post, Comment
from app.schemas.userSchema import users_schema
from app.utils.exc import handler, NotFound



@app.get('/admin')
@token_auth.login_required(role='admin')
@cache.cached(timeout=60)
@limiter.limit('100 per day')
@handler
def get_admin():
    query = db.select(Role).filter_by(name='admin')
    admin = db.session.scalar(query)
    if admin is None:
        raise NotFound("role named 'admin'")
    return users_schema.jsonify(admin.users)

@app.delete('/admin/users/<int:user_id>')
@token_auth.login_required(role='admin')
@handler
def delete_user_admin(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise NotFound(f"user with ID {user_id}")
    db.session.delete(user)
    db.session.commit()
    return {'success': f"The user with ID {user_id} is no more!"}

@app.delete('/admin/posts/<int:post_id>')
@token_auth.login_required(role='admin')
@handler
def delete_post_admin(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        raise NotFound(f"post with ID {post_id}")
    db.session.delete(post)
    db.session.commit()
    return {'success': f"The post with ID {post_id} is no more!"}

@app.delete('/admin/comments/<int:comment_id>')
@token_auth.login_required(role='admin')
@handler
def delete_comment_admin(comment_id):
    comment = db.session.get(Comment, comment_id)
    if comment is None:
        raise NotFound(f"comment with ID {comment_id}")
    db.session.delete(comment)
    db.session.commit()
    return {'success': f"The comment with ID {comment_id} is no more!"}