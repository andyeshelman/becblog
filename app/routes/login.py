from flask import request

from app import app
from app.database import db
from app.models import User
from app.schemas.userSchema import user_schema_login
from app.utils.exc import handler, ContentType, BadLogin
from app.utils.password import check_password
from app.utils.token import encode_token


@app.post('/login')
@handler
def post_login():
    if not request.is_json:
        raise ContentType("application/json")
    creds = user_schema_login.load(request.json)
    query = db.select(User).filter_by(username=creds['username'])
    user = db.session.scalar(query)
    if user is None:
        raise BadLogin
    if not check_password(user, creds):
        raise BadLogin
    token = encode_token(user.id)
    return {'token': token}