import unittest
from fastapi.testclient import TestClient

from passiveDNS.db.database import get_db
from passiveDNS.models.user import User
from passiveDNS.models.user_request import UserRequest
from passiveDNS.webserver import app

client = TestClient(app)


class AdminUsersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()
        cls.db.clear()
        cls.db.connect()

        cls.admin1 = User(
            _key="TestAdmin1",
            email="admin1@test.com",
            hashed_password=User._hash_password("admin1"),
            role="admin",
            api_keys={},
        )
        cls.admin1.insert()

        cls.admin2 = User(
            _key="TestAdmin2",
            email="admin2@test.com",
            hashed_password=User._hash_password("admin2"),
            role="admin",
            api_keys={},
        )
        cls.admin2.insert()

        cls.user1Request = UserRequest.new("user1@test.com")
        cls.user1Request.insert()
        cls.user2Request = UserRequest.new("user2@test.com")
        cls.user2Request.insert()

        cls.user3 = User.new("TestUser3", "user3", "user3@test.com")
        cls.user3.insert()

        client.post("/apiv2/token", json={"identity": "TestAdmin1", "password": "admin1"})

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.clear()

    # /admin/request/list get
    def test_request_list(self) -> None:
        response = client.get("/apiv2/admin/request/list")
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_request_list", response.json())

    # /admin/request delete
    def test_request_delete(self) -> None:
        response = client.delete("/apiv2/admin/request/user2@test.com")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("user_request", data)

    def test_request_delete_not_found(self) -> None:
        response = client.delete("/apiv2/admin/request/none@test.com")
        self.assertEqual(response.status_code, 404)

    # /admin/invite/list get
    def test_pending_list(self) -> None:
        response = client.get("/apiv2/admin/invite/list")
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_pending_list", response.json())

    # /admin/users/list get
    def test_users_list(self) -> None:
        response = client.get("/apiv2/admin/users/list")
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_list", response.json())

    # /admin/users delete
    def test_user_delete(self) -> None:
        response = client.delete("/apiv2/admin/users/TestUser3")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("user", data)

    def test_user_delete_is_admin(self) -> None:
        response = client.delete("/apiv2/admin/users/TestAdmin2")
        self.assertEqual(response.status_code, 500)


# /admin/invite post : mail sending so manual testing

# /admin/verify post : mail sending so manual testing
