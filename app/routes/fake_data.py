from faker import Faker

from random import choice, randint

from app import app
from app.database import db
from app.models import User, Post
from app.utils.password import hash_password

fake = Faker('en-US')

@app.patch('/fake-data')
def gen_data():
    user_ids = []
    for _ in range(10):
        user = User()
        user.name = fake.name()
        user.username = (user.name[0] + user.name.split()[-1]).lower() + str(randint(1,999))
        user.password = user.username
        user.email = user.username + "@example.com"
        hash_password(user)
        db.session.add(user)
        db.session.flush()
        db.session.refresh(user)
        user_ids.append(user.id)
    
    for _ in range(100):
        post = Post()
        post.user_id = choice(user_ids)
        post.title = "RE: " + fake.color_name()
        post.body = "\n".join(fake.paragraphs(nb=5))
        db.session.add(post)
    
    db.session.commit()

    return {'succes': "Fake data has been generated and entered!"}