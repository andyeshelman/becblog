from flask import request

from app import app
from app.database import db
from app.models import Post
from app.schemas.postSchema import post_schema, posts_schema, post_schema_edit
from app.utils.exc import NotFound, ContentType, Forbidden, handler
from app.utils.auth import token_auth

@app.get('/posts')
def get_all_posts():
    query = db.select(Post)
    posts = db.paginate(query)
    return posts_schema.jsonify(posts)

@app.get('/posts/<int:post_id>')
@handler
def get_one_post(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        raise NotFound(f"post with ID {post_id}")
    return post_schema.jsonify(post)

@app.post('/posts')
@token_auth.login_required
@handler
def post_post():
    if not request.is_json:
        raise ContentType("application/json")
    post_data = post_schema_edit.load(request.json)
    user = token_auth.current_user()
    post = Post(**post_data)
    user.posts.append(post)
    db.session.commit()
    return post_schema.jsonify(post)

    
@app.put('/posts/<int:post_id>')
@token_auth.login_required
@handler
def put_post(post_id):
    if not request.is_json:
        raise ContentType("application/json")
    post = db.session.get(Post, post_id)
    if post is None:
        raise NotFound(f"post with ID {post_id}")
    user = token_auth.current_user()
    if not user is post.user:
        raise Forbidden("edit this post")
    diff_data = post_schema_edit.load(request.json, partial=True)
    for key, value in diff_data.items():
        setattr(post, key, value)
    db.session.commit()
    return post_schema.jsonify(post)

@app.delete('/posts/<int:post_id>')
@token_auth.login_required
@handler
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        raise NotFound(f"post with ID {post_id}")
    user = token_auth.current_user()
    if not user is post.user:
        raise Forbidden("delete this post")
    db.session.delete(post)
    db.session.commit()
    return {'success': f"The post with ID {post_id} is no more!"}