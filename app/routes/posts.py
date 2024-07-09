from flask import request

from app import app
from app.modules import db, token_auth, cache, limiter
from app.models import Post, Comment
from app.schemas.postSchema import post_schema, posts_schema, post_schema_edit
from app.schemas.commentSchema import comments_schema, comment_schema_body
from app.utils.exc import handler, NotFound, ContentType, Permission

@app.get('/posts')
@token_auth.login_required
@cache.cached(timeout=60, query_string=True)
@limiter.limit('100 per day')
def get_all_posts():
    query = db.select(Post)
    posts = db.paginate(query)
    return posts_schema.jsonify(posts)

@app.get('/posts/<int:post_id>')
@token_auth.login_required
@cache.cached(timeout=60)
@limiter.limit('100 per day')
@handler
def get_one_post(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        raise NotFound(f"post with ID {post_id}")
    return post_schema.jsonify(post)

@app.get('/posts/<int:post_id>/comments')
@token_auth.login_required
@cache.cached(timeout=60)
@limiter.limit('100 per day')
@handler
def get_posts_comments(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        raise NotFound(f"post with ID {post_id}")
    return comments_schema.jsonify(post.comments)

@app.post('/posts')
@token_auth.login_required
@limiter.limit('100 per day')
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

@app.post('/posts/<int:post_id>/comments')
@token_auth.login_required
@limiter.limit('100 per day')
@handler
def post_posts_comments(post_id):
    if not request.is_json:
        raise ContentType("application/json")
    post = db.session.get(Post, post_id)
    if post is None:
        raise NotFound(f"post with ID {post_id}")
    user = token_auth.current_user()
    comment_data = comment_schema_body.load(request.json)
    comment = Comment(**comment_data, post=post, user=user)
    db.session.add(comment)
    db.session.commit()
    return comments_schema.jsonify(post.comments)
    
@app.put('/posts/<int:post_id>')
@token_auth.login_required
@limiter.limit('100 per day')
@handler
def put_post(post_id):
    if not request.is_json:
        raise ContentType("application/json")
    post = db.session.get(Post, post_id)
    if post is None:
        raise NotFound(f"post with ID {post_id}")
    user = token_auth.current_user()
    if not user is post.user:
        raise Permission("edit this post")
    diff_data = post_schema_edit.load(request.json, partial=True)
    for key, value in diff_data.items():
        setattr(post, key, value)
    db.session.commit()
    return post_schema.jsonify(post)

@app.delete('/posts/<int:post_id>')
@token_auth.login_required
@limiter.limit('100 per day')
@handler
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        raise NotFound(f"post with ID {post_id}")
    user = token_auth.current_user()
    if not user is post.user:
        raise Permission("delete this post")
    db.session.delete(post)
    db.session.commit()
    return {'success': f"The post with ID {post_id} is no more!"}