from flask import request

from app import app
from app.modules import db, token_auth, cache, limiter
from app.models import User
from app.schemas.userSchema import user_schema, user_schema_nopass, users_schema, user_schema_edit
from app.schemas.postSchema import posts_schema
from app.schemas.commentSchema import comments_schema
from app.utils.exc import handler, Duplicate, NotFound, ContentType
from app.utils.password import hash_password

@app.get('/users')
@token_auth.login_required
@cache.cached(timeout=60)
@limiter.limit('100 per day')
def get_all_users():
    query = db.select(User)
    users = db.session.scalars(query)
    return users_schema.jsonify(users)

@app.get('/users/<int:user_id>')
@token_auth.login_required
@cache.cached(timeout=60)
@limiter.limit('100 per day')
@handler
def get_one_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise NotFound(f"user with ID {user_id}")
    return user_schema_nopass.jsonify(user)

@app.get('/users/<int:user_id>/posts')
@token_auth.login_required
@cache.cached(timeout=60)
@limiter.limit('100 per day')
@handler
def get_users_posts(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise NotFound(f"user with ID {user_id}")
    return posts_schema.jsonify(user.posts)

@app.get('/users/<int:user_id>/comments')
@token_auth.login_required
@cache.cached(timeout=60)
@limiter.limit('100 per day')
@handler
def get_users_comments(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise NotFound(f"user with ID {user_id}")
    return comments_schema.jsonify(user.comments)

@app.post('/users')
@limiter.limit('100 per day')
@handler
def post_user():
    if not request.is_json:
        raise ContentType("application/json")
    user_data = user_schema.load(request.json)
    username = user_data['username']
    query = db.select(User).filter_by(username=username)
    if db.session.scalar(query):
        raise Duplicate(f"username {username}")
    email = user_data['email']
    query = db.select(User).filter_by(email=email)
    if db.session.scalar(query):
        raise Duplicate(f"email {email}")
    user = User(**user_data)
    hash_password(user)
    db.session.add(user)
    db.session.commit()
    return user_schema_nopass.jsonify(user)

    
@app.put('/users')
@token_auth.login_required
@limiter.limit('100 per day')
@handler
def put_user():
    if not request.is_json:
        raise ContentType("application/json")
    user = token_auth.current_user()
    diff_data = user_schema_edit.load(request.json, partial=True)
    if 'username' in diff_data:
        username = diff_data['username']
        query = db.select(User).filter_by(username=username)
        if db.session.scalar(query):
            raise Duplicate(f"username {username}")
    if 'email' in diff_data:
        email = diff_data['email']
        query = db.select(User).filter_by(email=email)
        if db.session.scalar(query):
            raise Duplicate(f"email {email}")
    hash_password(diff_data)
    for key, value in diff_data.items():
        setattr(user, key, value)
    db.session.commit()
    return user_schema_nopass.jsonify(user)

@app.delete('/users')
@token_auth.login_required
@limiter.limit('100 per day')
@handler
def delete_user():
    user = token_auth.current_user()
    user_id = user.id
    db.session.delete(user)
    db.session.commit()
    return {'success': f"The user with ID {user_id} is no more!"}