import unittest
from unittest.mock import patch
from random import randint

from app import app
from app.modules import fake, db
from app.models import Comment
from app.schemas.commentSchema import comments_schema

class TestCommentsEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('flask_httpauth.HTTPTokenAuth.authenticate')
    @patch('app.routes.posts.db.paginate')
    def test_get_comments(self, mock_scalars, mock_auth):
        fake_comment = {
            'id': randint(1,999),
            'user_id': randint(1,999),
            'post_id': randint(1,999),
            'body': fake.text(),
        }
        mock_auth.return_value = True
        mock_scalars.return_value = [fake_comment]
        
        response = self.client.get('/comments')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(comments_schema.load(response.json), [fake_comment])

    def test_get_comments_notoken(self):
        response = self.client.get('/comments')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], "Invalid token...")

    @patch('flask_httpauth.HTTPTokenAuth.authenticate')
    def test_get_comment_99999(self, mock_auth):
        mock_auth.return_value = True
        response = self.client.get('/comments/99999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "A comment with ID 99999 does not exist...")

    @patch('flask_httpauth.HTTPTokenAuth.authenticate')
    def test_put_comment_nobody(self, mock_auth):
        mock_auth.return_value = True
        response = self.client.put(f'/comments/{randint(1,999)}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Request body must be application/json...")

    @patch('flask_httpauth.HTTPTokenAuth.authenticate')
    @patch('app.routes.comments.db.session.get')
    def test_put_comment_nopermission(self, mock_comment, mock_auth):
        mock_auth.return_value = True
        response = self.client.put(f'/comments/{randint(1,999)}', json={})
        self.assertEqual(response.status_code, 403)