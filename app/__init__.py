from flask import Flask

import os

from app.modules import db, migrate, cache, limiter, swaggerui_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.json.sort_keys = False

db.init_app(app)
migrate.init_app(app, db)
cache.init_app(app)
limiter.init_app(app)

app.register_blueprint(swaggerui_blueprint)

from . import routes, models
