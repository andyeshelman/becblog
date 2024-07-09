import unittest
from unittest.mock import MagicMock, patch

from app import app
from app.modules import fake
from app.schemas.userSchema import users_schema

class TestUsersEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('app.modules.auth.decode_token')
    @patch('app.modules.auth.db.session.get')
    @patch('app.routes.users.db.session.scalars')
    def test_get_users(self, mock_scalars, mock_get, mock_decode):
        fake_user = {
            'id': 1,
            'name': fake.name(),
            'email': fake.email(),
            'username': fake.user_name(),
        }
        mock_decode.return_value = None
        mock_get.return_value = True
        mock_scalars.return_value = [{**fake_user, 'password': fake.password()}]
        
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(users_schema.load(response.json), [fake_user])

    def test_get_users_notoken(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], "Invalid token...")