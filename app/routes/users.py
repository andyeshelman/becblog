from flask import request

from app import app
from app.database import db
from app.models import User
from app.schemas.userSchema import user_schema, user_schema_nopass, users_schema
from app.util import hash_password, Duplicate, NotFound, ContentType, handler

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

    
@app.put('/users/<int:user_id>')
@handler
def put_user(user_id):
    if not request.is_json:
        raise ContentType("application/json")
    user = db.session.get(User, user_id)
    if user is None:
        raise NotFound(f"user with ID {user_id}")
    user_data = user_schema.load(request.json, partial=True)
    if 'username' in user_data:
        username = user_data['username']
        query = db.select(User).filter_by(username=username)
        if db.session.scalar(query):
            raise Duplicate(f"username {username}")
    if 'email' in user_data:
        email = user_data['email']
        query = db.select(User).filter_by(email=email)
        if db.session.scalar(query):
            raise Duplicate(f"email {email}")
    hash_password(user_data)
    for key, value in user_data.items():
        setattr(user, key, value)
    db.session.commit()
    return user_schema_nopass.jsonify(user)

@app.delete('/users/<int:user_id>')
@handler
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise NotFound(f"user with ID {user_id}")
    db.session.delete(user)
    db.session.commit()
    return {'success': f"The user with ID {user_id} is no more!"}