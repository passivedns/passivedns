import unittest
from fastapi.testclient import TestClient

from passiveDNS.db.database import get_db
from passiveDNS.models.user import User
from passiveDNS.models.domain_name import DomainName
from passiveDNS.webserver import app

client = TestClient(app)


class ResolutionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()
        cls.user1 = User.new("TestUser1", "user1", "user1@test.com")
        cls.user1.insert()

        client.post("/token", json={"identity": "TestUser1", "password": "user1"})
        client.post("/dn/gitlab.esiea.fr")
        cls.dn1 = DomainName.get("gitlab.esiea.fr")
        cls.ip1 = cls.dn1.resolve()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.clear()

    # /resolution/{dn} get
    def test_get_resolution(self) -> None:
        response = client.get("/resolution/gitlab.esiea.fr")
        self.assertEqual(response.status_code, 200)
        self.assertIn("resolution", response.json())

    def test_get_resolution_not_found(self) -> None:
        response = client.get("/resolution/example.com")
        self.assertEqual(response.status_code, 404)

    # /resolution/{dn}/history get
    def test_get_resolution_history(self) -> None:
        response = client.get("/resolution/gitlab.esiea.fr/history")
        self.assertEqual(response.status_code, 200)
        self.assertIn("history", response.json())

    def test_get_resolution_history_not_found(self) -> None:
        response = client.get("/resolution/example.com/history")
        self.assertEqual(response.status_code, 404)

    # /reverse/{ip} get
    def test_get_reverse(self) -> None:
        response = client.get(f"/reverse/{self.ip1}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("resolution_list", response.json())

    def test_get_reverse_not_found(self) -> None:
        response = client.get("/reverse/1.2.3.4")
        self.assertEqual(response.status_code, 404)

    # /reverse/{ip}/history get
    def test_get_reverse_history(self) -> None:
        response = client.get(f"/reverse/{self.ip1}/history")
        self.assertEqual(response.status_code, 200)
        self.assertIn("history", response.json())

    def test_get_reverse_history_not_found(self) -> None:
        response = client.get("/reverse/1.2.3.4/history")
        self.assertEqual(response.status_code, 404)
