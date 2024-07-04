from .users import *
from .posts import *
from .login import post_login
from .fake_data import gen_data

@app.route('/')
def index():
    return "Let's goooooooooooo!"