import unittest
from unittest.mock import patch

from app import app
from app.modules import fake, db
from app.models import User
from app.schemas.userSchema import users_schema, user_schema

class TestUsersEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('flask_httpauth.HTTPTokenAuth.authenticate')
    @patch('app.routes.users.db.session.scalars')
    def test_get_users(self, mock_scalars, mock_auth):
        fake_user = {
            'id': 1,
            'name': fake.name(),
            'email': fake.email(),
            'username': fake.user_name(),
        }
        mock_auth.return_value = True
        mock_scalars.return_value = [{**fake_user, 'password': fake.password()}]
        
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(users_schema.load(response.json), [fake_user])

    def test_get_users_notoken(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], "Invalid token...")

    @patch('flask_httpauth.HTTPTokenAuth.authenticate')
    def test_get_user_99999(self, mock_auth):
        mock_auth.return_value = True
        response = self.client.get('/users/99999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "A user with ID 99999 does not exist...")

    @patch('flask_httpauth.HTTPTokenAuth.authenticate')
    def test_post_user_dupe(self, mock_auth):
        mock_auth.return_value = True
        with app.app_context():
            user = db.session.scalar(db.select(User))
            if user:
                mock_auth.return_value = user
                response = self.client.post('/users', json=user_schema.jsonify(user).json)
                self.assertEqual(response.status_code, 409)