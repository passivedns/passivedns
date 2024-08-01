import unittest
from fastapi.testclient import TestClient

from passiveDNS.db.database import get_db
from passiveDNS.models.user import User
from passiveDNS.webserver import app

client = TestClient(app)


class UsersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()
        cls.db.clear()
        cls.db.connect()

        cls.user1 = User.new(username="TestUser1", password="user1")
        cls.user1.insert()

        client.post("/apiv2/token", json={"identity": "TestUser1", "password": "user1"})

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.clear()

    # /password put
    def test_password(self) -> None:
        response = client.put(
            "/apiv2/password",
            json={"current_password": "user1", "new_password": "user1changed"},
        )
        self.assertEqual(response.status_code, 200)

    def test_password_invalid(self) -> None:
        response = client.put(
            "/apiv2/password",
            json={"current_password": "none", "new_password": "user1changed"},
        )
        self.assertEqual(response.status_code, 401)

    def test_password_same(self) -> None:
        response = client.put(
            "/apiv2/password",
            json={"current_password": "user1changed", "new_password": "user1changed"},
        )
        self.assertEqual(response.status_code, 400)

    # /apikey/{name} post
    # manual testing with api key

    # /apikey/{name} delete
