from flask_httpauth import HTTPTokenAuth

from app.utils.token import decode_token
from app.models import User
from app.modules import db

token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify(token):
    user_id = decode_token(token)
    try:
        return db.session.get(User, user_id)
    except Exception:
        return None

@token_auth.error_handler
def handle_error(status):
    if status == 403:
        return {'error': "You lack permission to perform this action..."}, 403
    else:
        return {'error': "Invalid token..."}, status

@token_auth.get_user_roles
def get_user_roles(user):
    return [role.name for role in user.roles]