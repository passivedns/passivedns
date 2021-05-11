from unittest import TestCase
from unittest.mock import MagicMock

from models.user import User, UserRole

username = 'dadard'
password = 'password'
hashed_password = 'stuff'
email = 'email'

role_user = UserRole.USER.value


class TestUser(TestCase):
    def test_init(self):
        u = User.new(username, password, email)
        self.assertEqual(u.username, username)
        self.assertEqual(u.email, email)
        self.assertNotEqual(u.hashed_password, password)

    def test_json(self):
        u = User.new(username, password, email)
        expected_json = {
            "_key": username,
            "hashed_password": hashed_password,
            "email": email,
            "role": role_user
        }
        actual_json = u.json()
        self.assertEqual(actual_json['_key'], expected_json['_key'])
        self.assertEqual(actual_json['email'], expected_json['email'])

    def test_exists_true(self):
        User._exists = MagicMock(return_value=True)
        self.assertTrue(User.exists(username))

    def test_exists_false(self):
        User._exists = MagicMock(return_value=False)
        self.assertFalse(User.exists(username))

    def test_get(self):
        example_json = {
            "_key": username,
            "hashed_password": hashed_password,
            "email": email,
            "role": role_user
        }
        User._get = MagicMock(return_value=example_json)
        u = User.get(username)
        self.assertEqual(u.username, example_json['_key'])
        self.assertEqual(u.hashed_password, hashed_password)
