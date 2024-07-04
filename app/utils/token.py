import jwt
import os
from datetime import datetime, timedelta, timezone

SECRET = os.environ.get('SECRET') or 'Gate Gate Paragate Parasamgate Bodhi Svaha'

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(timezone.utc),
        'customer_id': customer_id
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        return payload.get('customer_id')
    except Exception:
        return None