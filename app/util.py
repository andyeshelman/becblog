from werkzeug.security import generate_password_hash
from marshmallow import ValidationError
from sqlalchemy.exc import DatabaseError

from functools import wraps

def hash_password(obj):
    if isinstance(obj, dict) and 'password' in obj:
        obj['password'] = generate_password_hash(obj['password'])
    elif hasattr(obj, 'password'):
        obj.password = generate_password_hash(obj.password)

class Duplicate(Exception):
    def __init__(self, thing):
        self.message = {
            'error': f"The {thing} is already in use..."
        }

class NotFound(Exception):
    def __init__(self, thing):
        self.message = {
            'error': f"A {thing} does not exist..."
        }

class ContentType(Exception):
    def __init__(self, thing):
        self.message = {
            'error': f"Request body must be {thing}"
        }

def handler(func):
    @wraps(func)
    def handled(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ContentType as err:
            return err.message, 400
        except ValidationError as err:
            return err.messages, 400
        except Duplicate as err:
            return err.message, 400
        except NotFound as err:
            return err.message, 404
        except DatabaseError as err:
            return {'error': err.orig.msg}, 500
    return handled
