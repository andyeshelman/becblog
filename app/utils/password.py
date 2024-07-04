from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(obj):
    if isinstance(obj, str):
        return generate_password_hash(obj)
    elif isinstance(obj, dict) and 'password' in obj:
        obj['password'] = generate_password_hash(obj['password'])
    elif hasattr(obj, 'password'):
        obj.password = generate_password_hash(obj.password)

def check_password(objhash, objplain):
    if isinstance(objhash, str):
        hashed = objhash
    elif isinstance(objhash, dict) and 'password' in objhash:
        hashed = objhash['password']
    elif hasattr(objhash, 'password'):
        hashed = objhash.password
    
    if isinstance(objplain, str):
        plain = objplain
    elif isinstance(objplain, dict) and 'password' in objplain:
        plain = objplain['password']
    elif hasattr(objplain, 'password'):
        plain = objplain.password

    return check_password_hash(hashed, plain)