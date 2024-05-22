import unittest
from fastapi.testclient import TestClient

from db.database import get_db
from models.user import User
from main import app

client = TestClient(app)

class AuthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()
        cls.admin1 = User(
            _key="TestAdmin1", email="admin1@test.com",
            hashed_password=User._hash_password("admin1"), role="Admin"
        )
        cls.admin1.insert()

        cls.user1 = User.new(username="TestUser1", password="user1", email="user1@test.com")
        cls.user1.insert()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.admin1.delete()
        cls.user1.delete()
    

    def test_login(self) -> None:
        response = client.post("/token", json={"identity":"TestUser1", "password":"user1"})
        self.assertEqual(response.status_code, 200)