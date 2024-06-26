import unittest
from fastapi.testclient import TestClient

from passiveDNS.db.database import get_db
from passiveDNS.models.user import User
from passiveDNS.models.user_pending import UserPending
from passiveDNS.models.user_request import UserRequest
from passiveDNS.webserver import app

client = TestClient(app)


class UsersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()
        cls.db.connect()
        cls.db.clear()

        cls.user1 = User.new(
            username="TestUser1", password="user1", email="user1@test.com"
        )
        cls.user1.insert()
        cls.user2Pending = UserPending.new("user2@test.com")
        cls.user3Pending = UserPending.new("user3@test.com")
        cls.user2Token = cls.user2Pending.token
        cls.user2Pending.insert()
        cls.user3Pending.insert()
        client.post("/token", json={"identity": "TestUser1", "password": "user1"})

    @classmethod
    def tearDownClass(cls) -> None:
        client.get("/logout")
        cls.db.clear()

    # /register post
    def test_register(self) -> None:
        response = client.post(
            "/register",
            json={
                "username": "TestUser2",
                "password": "user2",
                "token": self.user2Token,
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["msg"], "user TestUser2 created")
        self.assertIn("user", data)

    def test_register_username_taken(self) -> None:
        response = client.post(
            "/register",
            json={
                "username": "TestUser1",
                "password": "user1",
                "token": self.user2Token,
            },
        )
        self.assertEqual(response.status_code, 500)

    def test_register_no_token(self) -> None:
        response = client.post(
            "/register",
            json={"username": "TestUser3", "password": "user3", "token": ""},
        )
        self.assertEqual(response.status_code, 404)

    # /register/check post
    def test_token_check(self) -> None:
        response = client.post(
            "/register/check", json={"token": self.user3Pending.token}
        )
        self.assertEqual(response.status_code, 200)

    def test_token_check_invalid(self) -> None:
        response = client.post("/register/check", json={"token": self.user2Token})
        self.assertEqual(response.status_code, 400)

    # /request post
    def test_request(self) -> None:
        response = client.post("/request", json={"email": "user4@test.com"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(
            data["msg"], "request for access with mail user4@test.com sent to admin"
        )
        self.assertIn("user_request", data)

    def test_request_email_unavailable(self) -> None:
        response = client.post("/request", json={"email": "user1@test.com"})
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertEqual(data["detail"], "email unavailable")

    def test_request_pending_exists(self) -> None:
        response = client.post("/request", json={"email": "user3@test.com"})
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertEqual(
            data["detail"], "an invitation has already been sent to this email"
        )

    def test_request_already_exists(self) -> None:
        response = client.post("/request", json={"email": "user4@test.com"})
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertEqual(
            data["detail"], "a request for this email has already been sent"
        )

    # /password put
    def test_password(self) -> None:
        response = client.put(
            "/password",
            json={"current_password": "user1", "new_password": "user1changed"},
        )
        self.assertEqual(response.status_code, 200)

    def test_password_invalid(self) -> None:
        response = client.put(
            "/password",
            json={"current_password": "none", "new_password": "user1changed"},
        )
        self.assertEqual(response.status_code, 401)

    def test_password_same(self) -> None:
        response = client.put(
            "/password",
            json={"current_password": "user1changed", "new_password": "user1changed"},
        )
        self.assertEqual(response.status_code, 400)

    # /apikey/{name} post
    # manual testing with api key

    # /apikey/{name} delete
