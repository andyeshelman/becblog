from flask import request

from app import app
from app.database import db
from app.models import User
from app.schemas.userSchema import user_schema, user_schema_nopass, users_schema, user_schema_edit
from app.utils.exc import Duplicate, NotFound, ContentType, handler
from app.utils.password import hash_password
from app.utils.auth import token_auth

@app.get('/users')
def get_all_users():
    query = db.select(User)
    users = db.session.scalars(query)
    return users_schema.jsonify(users)

@app.get('/users/<int:user_id>')
@handler
def get_one_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise NotFound(f"user with ID {user_id}")
    return user_schema_nopass.jsonify(user)

@app.post('/users')
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
@handler
def delete_user():
    user = token_auth.current_user()
    user_id = user.id
    db.session.delete(user)
    db.session.commit()
    return {'success': f"The user with ID {user_id} is no more!"}