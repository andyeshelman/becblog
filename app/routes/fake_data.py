from flask import request

from random import choice, randint

from app import app
from app.modules import db, fake, limiter
from app.models import User, Post, Comment, Role
from app.schemas.userSchema import user_schema_nopass, users_schema
from app.schemas.postSchema import posts_schema
from app.schemas.commentSchema import comments_schema
from app.utils.password import hash_password
from app.utils.exc import handler

@app.patch('/fake-data/admin')
@limiter.limit('5 per day')
@handler
def fake_admin():
    query = db.select(Role).filter_by(name='admin')
    admin = db.session.scalar(query)
    if admin is None:
        admin = Role(name='admin')
        db.session.add(admin)
    user = User()
    user.name = fake.name()
    user.email = fake.email()
    user.username = "admin" + str(randint(1,999))
    user.password = hash_password(user.username)
    user.roles.append(admin)
    db.session.add(user)
    db.session.commit()
    return user_schema_nopass.jsonify(user)

@app.patch('/fake-data/users')
@limiter.limit('5 per day')
@handler
def fake_users():
    nb = request.args.get('nb', 1, type=int)
    nb = min(nb, 20)

    for _ in range(nb):
        user = User()
        user.name = fake.name()
        user.username = (user.name[0] + user.name.split()[-1]).lower() + str(randint(1,999))
        user.password = user.username
        user.email = user.username + "@example.com"
        hash_password(user)
        db.session.add(user)

    db.session.commit()

    return {'success': "Fake users have been generated!"}
    
@app.patch('/fake-data/posts')
@limiter.limit('5 per day')
def fake_posts():
    nb = request.args.get('nb', 1, type=int)
    nb = min(nb, 20)
    q = db.select(User)
    users = db.session.scalars(q).all()

    for _ in range(nb):
        post = Post()
        post.user = choice(users)
        post.title = "RE: " + fake.color_name()
        post.body = "\n".join(fake.paragraphs(nb=5))
        db.session.add(post)
    
    db.session.commit()

    return {'success': "Fake posts have been generated!"}

@app.patch('/fake-data/comments')
@limiter.limit('5 per day')
def fake_comments():
    nb = request.args.get('nb', 1, type=int)
    nb = min(nb, 20)
    q = db.select(User)
    users = db.session.scalars(q).all()
    q = db.select(Post)
    posts = db.session.scalars(q).all()

    for _ in range(nb):
        comment = Comment()
        comment.user = choice(users)
        comment.post = choice(posts)
        comment.body = fake.paragraph()
        db.session.add(comment)
    
    db.session.commit()

    return {'success': "Fake comments have been generated!"}