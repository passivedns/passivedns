import unittest
from fastapi.testclient import TestClient

from passiveDNS.db.database import get_db
from passiveDNS.models.user import User
from passiveDNS.webserver import app

client = TestClient(app)


class AuthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()
        cls.db.clear()
        cls.db.connect()

        cls.admin1 = User(
            _key="TestAdmin1",
            hashed_password=User._hash_password("admin1"),
            role="admin",
            api_keys={},
        )
        cls.admin1.insert()

        cls.user1 = User.new(username="TestUser1", password="user1")
        cls.user1.insert()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.clear()

    def test_login_admin(self) -> None:
        response = client.post(
            "/apiv2/token", json={"identity": "TestAdmin1", "password": "admin1"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["token_type"], "bearer")
        self.assertIn("set-cookie", response.headers)
        self.assertIn("passiveDNS_session", response.headers["set-cookie"])
        self.assertIn(data["access_token"], response.headers["set-cookie"])

    def test_login_user(self) -> None:
        response = client.post(
            "/apiv2/token", json={"identity": "TestUser1", "password": "user1"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["token_type"], "bearer")
        self.assertIn("set-cookie", response.headers)
        self.assertIn("passiveDNS_session", response.headers["set-cookie"])
        self.assertIn(data["access_token"], response.headers["set-cookie"])

    def test_login_not_user(self) -> None:
        response = client.post(
            "/apiv2/token", json={"identity": "random", "password": "user"}
        )
        self.assertEqual(response.status_code, 404)

    def test_login_wrong_password(self) -> None:
        response = client.post(
            "/apiv2/token", json={"identity": "TestUser1", "password": "random"}
        )
        self.assertEqual(response.status_code, 401)

    def test_token(self) -> None:
        client.post("/apiv2/token", json={"identity": "TestUser1", "password": "user1"})
        response = client.get("/apiv2/token")
        self.assertEqual(response.status_code, 200)

    def test_token_invalid(self) -> None:
        client.get("/apiv2/logout")
        response = client.get("/apiv2/token")
        self.assertEqual(response.status_code, 400)

    def test_logout(self) -> None:
        response = client.get("/apiv2/logout")
        self.assertEqual(response.status_code, 200)
