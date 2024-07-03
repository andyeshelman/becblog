from flask import Flask

import os

from app.database import db, migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.json.sort_keys = False

db.init_app(app)
migrate.init_app(app, db)

from . import routes, models
