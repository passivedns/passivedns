from unittest import TestCase
from unittest.mock import MagicMock

from passiveDNS.models.user import User, UserRole
from passiveDNS.db.database import get_db
from passiveDNS.utils import config

config.init_config()

username = "dadard"
password = "password"
hashed_password = "stuff"
email = "email"

role_user = UserRole.USER.value


class TestUser(TestCase):
    def setUp(self):
        self.db = get_db()
        self.db.connect()
        self.db.clear()
        
    def tearDown(self):
        self.db.clear()
        
    def test_init_user(self):
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
            "role": role_user,
            "api_keys": {},
        }
        actual_json = u.json()
        self.assertEqual(actual_json["_key"], expected_json["_key"])
        self.assertEqual(actual_json["email"], expected_json["email"])

    def test_exists_true(self):
        User._exists = MagicMock(return_value=True)
        self.assertTrue(User.exists(username))

    def test_exists_false(self):
        User._exists = MagicMock(return_value=False)
        self.assertFalse(User.exists(username))

    def test_get_user(self):
        example_json = {
            "_key": username,
            "hashed_password": hashed_password,
            "email": email,
            "role": role_user,
            "api_keys": {},
        }
        User._get = MagicMock(return_value=example_json)
        u = User.get(username)
        self.assertEqual(u.username, example_json["_key"])
        self.assertEqual(u.hashed_password, hashed_password)
