import unittest
from fastapi.testclient import TestClient

from passiveDNS.db.database import get_db
from passiveDNS.models.user import User
from passiveDNS.models.domain_name import DomainName
from passiveDNS.webserver import app

client = TestClient(app)


class InfoAlertTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()
        cls.db.connect()
        cls.db.clear()

        cls.user1 = User.new("TestUser1", "user1", "user1@test.com")
        cls.user1.insert()

        cls.dn1 = DomainName.new("dns.google.com")
        cls.dn1.insert()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.clear()

    # /alert get
    def test_alert_list(self) -> None:
        client.post("/token", json={"identity": "TestUser1", "password": "user1"})
        response = client.get(
            "/alert",
            params={
                "filter": "dns.google.com",
                "filter_by": "domainName",
                "sort_by": "domainName",
                "limit": "10",
                "days": "10",
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("dn_list", data)
        self.assertIn("stats", data)
        self.assertIn("transaction_time", data["stats"])
        self.assertIn("count", data["stats"])
        client.get("/logout")

    def test_alert_list_invalid_limit(self) -> None:
        client.post("/token", json={"identity": "TestUser1", "password": "user1"})
        response = client.get(
            "/alert",
            params={
                "filter": "dns.google.com",
                "filter_by": "domainName",
                "sort_by": "domainName",
                "limit": "no",
                "days": "10",
            },
        )
        self.assertEqual(response.status_code, 400)
        client.get("/logout")

    def test_alert_list_invalid_days(self) -> None:
        client.post("/token", json={"identity": "TestUser1", "password": "user1"})
        response = client.get(
            "/alert",
            params={
                "filter": "dns.google.com",
                "filter_by": "domainName",
                "sort_by": "domainName",
                "limit": "10",
                "days": "no",
            },
        )
        self.assertEqual(response.status_code, 400)
        client.get("/logout")

    def test_alert_list_invalid_filter(self) -> None:
        client.post("/token", json={"identity": "TestUser1", "password": "user1"})
        response = client.get(
            "/alert",
            params={
                "filter": "dns.google.com",
                "filter_by": "domain",
                "sort_by": "domainName",
                "limit": "10",
                "days": "10",
            },
        )
        self.assertEqual(response.status_code, 400)
        client.get("/logout")

    def test_alert_list_invalid_sort(self) -> None:
        client.post("/token", json={"identity": "TestUser1", "password": "user1"})
        response = client.get(
            "/alert",
            params={
                "filter": "dns.google.com",
                "filter_by": "domainName",
                "sort_by": "domain",
                "limit": "10",
                "days": "10",
            },
        )
        self.assertEqual(response.status_code, 400)

    # /alert/export get
    def test_alert_list_export_csv(self) -> None:
        client.post("/token", json={"identity": "TestUser1", "password": "user1"})
        response = client.get(
            "/alert/export",
            params={
                "filter": "dns.google.com",
                "filter_by": "domainName",
                "sort_by": "domainName",
                "limit": "10",
                "days": "10",
                "export": "csv",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/csv")
        client.get("/logout")

    def test_alert_list_export_json(self) -> None:
        client.post("/token", json={"identity": "TestUser1", "password": "user1"})
        response = client.get(
            "/alert/export",
            params={
                "filter": "dns.google.com",
                "filter_by": "domainName",
                "sort_by": "domainName",
                "limit": "10",
                "days": "10",
                "export": "json",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        client.get("/logout")

    def test_alert_list_export_invalid_export_field(self) -> None:
        client.post("/token", json={"identity": "TestUser1", "password": "user1"})
        response = client.get(
            "/alert/export",
            params={
                "filter": "dns.google.com",
                "filter_by": "domainName",
                "sort_by": "domainName",
                "limit": "10",
                "days": "10",
                "export": "yes",
            },
        )
        self.assertEqual(response.status_code, 400)
        client.get("/logout")

    # infos
    # /infos get
    def test_get_infos(self) -> None:
        response = client.get("/infos")
        self.assertEqual(response.status_code, 200)
        self.assertIn("version", response.json())
        self.assertIn("job_url", response.json())
        self.assertIn("commit_sha", response.json())
