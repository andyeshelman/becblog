from flask import request

from app import app
from app.database import db
from app.models import Post
from app.schemas.postSchema import post_schema, posts_schema
from app.util import Duplicate, NotFound, ContentType, handler

@app.get('/posts')
def get_all_posts():
    query = db.select(Post)
    posts = db.session.scalars(query)
    return posts_schema.jsonify(posts)

@app.get('/posts/<int:post_id>')
@handler
def get_one_post(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        raise NotFound(f"post with ID {post_id}")
    return post_schema.jsonify(post)

@app.post('/posts')
@handler
def post_post():
    if not request.is_json:
        raise ContentType("application/json")
    post_data = post_schema.load(request.json)
    post = Post(**post_data)
    db.session.add(post)
    db.session.commit()
    return post_schema.jsonify(post)

    
@app.put('/posts/<int:post_id>')
@handler
def put_post(post_id):
    if not request.is_json:
        raise ContentType("application/json")
    post = db.session.get(Post, post_id)
    if post is None:
        raise NotFound(f"post with ID {post_id}")
    post_data = post_schema.load(request.json, partial=True)
    for key, value in post_data.items():
        setattr(post, key, value)
    db.session.commit()
    return post_schema.jsonify(post)

@app.delete('/posts/<int:post_id>')
@handler
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        raise NotFound(f"post with ID {post_id}")
    db.session.delete(post)
    db.session.commit()
    return {'success': f"The post with ID {post_id} is no more!"}