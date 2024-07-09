from .users import *
from .posts import *
from .comments import *
from .login import post_login
from .fake_data import *
from .admin import *

from flask import redirect

@app.route('/')
def index():
    return redirect('/api/docs')