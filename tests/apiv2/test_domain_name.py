import unittest
from fastapi.testclient import TestClient

from passiveDNS.db.database import get_db
from passiveDNS.models.user import User
from passiveDNS.models.domain_name import DomainName
from passiveDNS.models.users_dn import UserDn
from passiveDNS.webserver import app

client = TestClient(app)


class DomainNameTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()
        cls.db.connect()
        cls.db.clear()

        cls.user1 = User.new("TestUser1", "user1", "user1@test.com")
        cls.user1.insert()

        client.post("/apiv2/token", json={"identity": "TestUser1", "password": "user1"})

        cls.dn1 = DomainName.new("esiea.fr")
        cls.dn1.insert()
        cls.userdn1 = UserDn.new("TestUser1", "esiea.fr", True)
        cls.userdn1.insert()

        cls.dn2 = DomainName.new("bing.com")
        cls.dn2.insert()
        cls.userdn2 = UserDn.new("TestUser2", "bing.com", True)
        cls.userdn2.insert()

        cls.dn3 = DomainName.new("example.com")
        cls.dn3.insert()
        cls.userdn3 = UserDn.new("TestUser2", "example.com", True)
        cls.userdn3.insert()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.clear()

    # /dn get
    def test_dn_list(self) -> None:
        response = client.get(
            "/apiv2/dn",
            params={
                "filter": "google.com",
                "filter_by": "ipAddress",
                "sort_by": "domainName",
                "limit": "10",
                "owned": "false",
                "followed": "false",
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("dn_list", data)
        self.assertIn("stats", data)
        self.assertIn("transaction_time", data["stats"])
        self.assertIn("count", data["stats"])

    def test_dn_list_invalid_limit(self) -> None:
        response = client.get(
            "/apiv2/dn",
            params={
                "filter": "google.com",
                "filter_by": "ipAddress",
                "sort_by": "domainName",
                "limit": "no",
                "owned": "false",
                "followed": "false",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_dn_list_invalid_filter(self) -> None:
        response = client.get(
            "/apiv2/dn",
            params={
                "filter": "google.com",
                "filter_by": "ip",
                "sort_by": "domainName",
                "limit": "10",
                "owned": "false",
                "followed": "false",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_dn_list_invalid_sort(self) -> None:
        response = client.get(
            "/apiv2/dn",
            params={
                "filter": "google.com",
                "filter_by": "ipAddress",
                "sort_by": "domain",
                "limit": "10",
                "owned": "false",
                "followed": "false",
            },
        )
        self.assertEqual(response.status_code, 400)

    # /dn/export get
    def test_dn_list_export_csv(self) -> None:
        response = client.get(
            "/apiv2/dn/export",
            params={
                "filter": "google.com",
                "filter_by": "ipAddress",
                "sort_by": "domainName",
                "limit": "10",
                "owned": "false",
                "followed": "false",
                "export": "csv",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/csv")

    def test_dn_list_export_json(self) -> None:
        response = client.get(
            "/apiv2/dn/export",
            params={
                "filter": "google.com",
                "filter_by": "ipAddress",
                "sort_by": "domainName",
                "limit": "10",
                "owned": "false",
                "followed": "false",
                "export": "json",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

    # /dn/{domain_name} post
    def test_dn_create(self) -> None:
        response = client.post("/apiv2/dn/dns.google.com")
        self.assertEqual(response.status_code, 200)
        self.assertIn("dn", response.json())

    def test_dn_create_already_exists(self) -> None:
        response = client.post("/apiv2/dn/esiea.fr")
        self.assertEqual(response.status_code, 500)

    def test_dn_create_not_resolved(self) -> None:
        response = client.post("/apiv2/dn/test")
        self.assertEqual(response.status_code, 500)

    # /dn/{domain_name} get
    def test_dn_get(self) -> None:
        response = client.get("/apiv2/dn/example.com")
        self.assertEqual(response.status_code, 200)
        self.assertIn("dn", response.json())
        self.assertIn("dn_tags", response.json())
        self.assertIn("ip", response.json())
        self.assertIn("ip_tags", response.json())
        self.assertIn("owned", response.json())
        self.assertIn("followed", response.json())

    def test_dn_get_not_found(self) -> None:
        response = client.get("/apiv2/dn/test.com")
        self.assertEqual(response.status_code, 404)

    # /dn/{domain_name} put
    def test_dn_update(self) -> None:
        response = client.put("/apiv2/dn/example.com")
        self.assertEqual(response.status_code, 200)
        self.assertIn("dn", response.json())

    def test_dn_update_not_found(self) -> None:
        response = client.put("/apiv2/dn/test.com")
        self.assertEqual(response.status_code, 404)

    # /dn/{domain_name} delete
    def test_dn_delete(self) -> None:
        response = client.delete("/apiv2/dn/dns.google.com")
        self.assertEqual(response.status_code, 200)
        self.assertIn("dn", response.json())

    def test_dn_delete_not_owned(self) -> None:
        response = client.delete("/apiv2/dn/bing.com")
        self.assertEqual(response.status_code, 403)

    # /dn/{dn}/follow post
    def test_dn_follow(self) -> None:
        response = client.post("/apiv2/dn/bing.com/follow")
        self.assertEqual(response.status_code, 200)

    def test_dn_follow_already_following(self) -> None:
        response = client.post("/apiv2/dn/esiea.fr/follow")
        self.assertEqual(response.status_code, 500)

    # /dn/{dn}/follow delete
    def test_dn_follow_remove(self) -> None:
        response = client.delete("/apiv2/dn/esiea.fr/follow")
        self.assertEqual(response.status_code, 200)

    def test_dn_follow_remove_not_following(self) -> None:
        response = client.delete("/apiv2/dn/example.com/follow")
        self.assertEqual(response.status_code, 404)
