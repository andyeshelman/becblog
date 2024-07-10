import unittest
from unittest.mock import patch
from random import randint

from app import app
from app.modules import fake, db
from app.models import Post
from app.schemas.postSchema import posts_schema

class TestPostsEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('flask_httpauth.HTTPTokenAuth.authenticate')
    @patch('app.routes.posts.db.paginate')
    def test_get_posts(self, mock_scalars, mock_auth):
        fake_post = {
            'id': randint(1,999),
            'user_id': randint(1,999),
            'title': fake.color_name(),
            'body': fake.text(),
        }
        mock_auth.return_value = True
        mock_scalars.return_value = [fake_post]
        
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(posts_schema.load(response.json), [fake_post])

    def test_get_posts_notoken(self):
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], "Invalid token...")

    @patch('flask_httpauth.HTTPTokenAuth.authenticate')
    def test_get_post_99999(self, mock_auth):
        mock_auth.return_value = True
        response = self.client.get('/posts/99999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "A post with ID 99999 does not exist...")
    
    @patch('flask_httpauth.HTTPTokenAuth.authenticate')
    def test_post_post_nobody(self, mock_auth):
        mock_auth.return_value = True
        response = self.client.post('/posts')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Request body must be application/json...")

    @patch('flask_httpauth.HTTPTokenAuth.authenticate')
    def test_delete_post_nopermission(self, mock_auth):
        mock_auth.return_value = True
        with app.app_context():
            post = db.session.scalar(db.select(Post))
            response = self.client.delete(f'/posts/{post.id}')
            self.assertEqual(response.status_code, 403)