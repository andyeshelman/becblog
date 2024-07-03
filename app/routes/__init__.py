from .users import *
from .posts import *

@app.route('/')
def index():
    return "Let's goooooooooooo!"