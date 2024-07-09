from marshmallow import ValidationError
from sqlalchemy.exc import DatabaseError

from functools import wraps

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
            'error': f"Request body must be {thing}..."
        }

class BadLogin(Exception):
    def __init__(self):
        self.message = {
            'error': "This username and/or password is invalid..."
        }

class Permission(Exception):
    def __init__(self, thing):
        self.message = {
            'error': f"You do not have permission to {thing}..."
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
        except BadLogin as err:
            return err.message, 401
        except Permission as err:
            return err.message, 403
        except NotFound as err:
            return err.message, 404
        except Duplicate as err:
            return err.message, 409
        except DatabaseError as err:
            return {'error': err.orig.msg}, 500
    return handled
