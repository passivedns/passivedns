import unittest
from fastapi.testclient import TestClient

from passiveDNS.db.database import get_db
from passiveDNS.models.user import User
from passiveDNS.models.domain_name import DomainName
from passiveDNS.webserver import app

client = TestClient(app)


class SchedulerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()
        cls.db.connect()
        cls.db.clear()

        cls.user1 = User.new("TestSched1", "sched1", "sched1@test.com", True)
        cls.user1.insert()

        cls.admin1 = User(
            _key="TestAdmin1",
            email="admin1@test.com",
            hashed_password=User._hash_password("admin1"),
            role="admin",
            api_keys={},
        )
        cls.admin1.insert()

        cls.dn1 = DomainName.new("example.com")
        cls.dn1.insert()

    @classmethod
    def tearDownClass(cls) -> None:
       cls.db.clear()

    # /scheduler/alerts get
    def test_get_alerts(self) -> None:
        client.post("/apiv2/token", json={"identity": "TestSched1", "password": "sched1"})
        response = client.get("/apiv2/scheduler/alerts")
        self.assertEqual(response.status_code, 200)
        self.assertIn("dn_list", response.json())
        client.get("/apiv2/logout")

    # /scheduler/alerts post : mail sending so manual testing

    # /scheduler/dn/{dn} put
    def test_dn_update(self) -> None:
        client.post("/apiv2/token", json={"identity": "TestSched1", "password": "sched1"})
        response = client.put("/apiv2/scheduler/dn/example.com")
        self.assertEqual(response.status_code, 200)
        self.assertIn("dn", response.json())
        client.get("/apiv2/logout")

    def test_dn_update_not_found(self) -> None:
        client.post("/apiv2/token", json={"identity": "TestSched1", "password": "sched1"})
        response = client.put("/apiv2/scheduler/dn/test.com")
        self.assertEqual(response.status_code, 404)
        client.get("/apiv2/logout")

    # /admin/scheduler/{name} post
    def test_admin_create_scheduler(self) -> None:
        client.post("/apiv2/token", json={"identity": "TestAdmin1", "password": "admin1"})
        response = client.post(
            "/apiv2/admin/scheduler/TestSched2", json={"password": "sched2"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("scheduler", response.json())
        client.get("/apiv2/logout")

    def test_admin_create_scheduler_name_taken(self) -> None:
        client.post("/apiv2/token", json={"identity": "TestAdmin1", "password": "admin1"})
        response = client.post(
            "/apiv2/admin/scheduler/TestSched1", json={"password": "sched3"}
        )
        self.assertEqual(response.status_code, 500)
        client.get("/apiv2/logout")

    # /admin/scheduler/{name} put
    def test_admin_update_scheduler_password(self) -> None:
        client.post("/apiv2/token", json={"identity": "TestAdmin1", "password": "admin1"})
        response = client.put("/apiv2/admin/scheduler/TestSched2", json={"password": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("scheduler", response.json())
        client.get("/apiv2/logout")

    def test_admin_update_scheduler_not_found(self) -> None:
        client.post("/apiv2/token", json={"identity": "TestAdmin1", "password": "admin1"})
        response = client.put("/apiv2/admin/scheduler/Test", json={"password": "sched2"})
        self.assertEqual(response.status_code, 404)
        client.get("/apiv2/logout")
