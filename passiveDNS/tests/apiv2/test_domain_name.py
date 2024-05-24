import unittest
from fastapi.testclient import TestClient

from db.database import get_db
from models.user import User
from models.ip_address import IPAddress
from models.domain_name import DomainName
from models.users_dn import UserDn
from main import app

client = TestClient(app)

class AuthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()

        cls.user1 = User.new("TestUser1", "user1", "user1@test.com")
        cls.user1.insert()

        client.post("/token", json={"identity":"TestUser1", "password":"user1"})
        
        cls.dn1 = DomainName.new("esiea.fr")
        cls.dn1.insert()

    @classmethod
    def tearDownClass(cls) -> None:
        UserDn.get("TestUser1", "dns.google.com").delete()
        client.get("/logout")
        cls.user1.delete()
        cls.dn1.delete()

        DomainName.get("dns.google.com").delete()
        cls.list = IPAddress.list()
        for ip in cls.list:
            ip.delete()


#/dn get
    def test_dn_list(self) -> None:
        response = client.get("/dn", params={
            "filter":"google.com",
            "filter_by": "ipAddress", 
            "sort_by": "domainName", 
            "limit": "10",  
            "owned": "false", 
            "followed": "false", 
            })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("dn_list", data)
        self.assertIn("stats", data)
        self.assertIn("transaction_time", data["stats"])
        self.assertIn("count", data["stats"])
    
    def test_dn_list_invalid_limit(self) -> None:
        response = client.get("/dn", params={
            "filter":"google.com",
            "filter_by": "ipAddress", 
            "sort_by": "domainName", 
            "limit": "no",  
            "owned": "false", 
            "followed": "false", 
            })
        self.assertEqual(response.status_code, 400)

    def test_dn_list_invalid_filter(self) -> None:
        response = client.get("/dn", params={
            "filter":"google.com",
            "filter_by": "ip", 
            "sort_by": "domainName", 
            "limit": "10",  
            "owned": "false", 
            "followed": "false", 
            })
        self.assertEqual(response.status_code, 400)

    def test_dn_list_invalid_sort(self) -> None:
        response = client.get("/dn", params={
            "filter":"google.com",
            "filter_by": "ipAddress", 
            "sort_by": "domain", 
            "limit": "10",  
            "owned": "false", 
            "followed": "false", 
            })
        self.assertEqual(response.status_code, 400)

#/dn/export get
    def test_dn_list_export_csv(self) -> None:
        response = client.get("/dn/export", params={
            "filter":"google.com",
            "filter_by": "ipAddress", 
            "sort_by": "domainName", 
            "limit": "10",  
            "owned": "false", 
            "followed": "false",
            "export":"csv"
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/csv")
    
    def test_dn_list_export_json(self) -> None:
        response = client.get("/dn/export", params={
            "filter":"google.com",
            "filter_by": "ipAddress", 
            "sort_by": "domainName", 
            "limit": "10",  
            "owned": "false", 
            "followed": "false",
            "export":"json"
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

#/dn/{domain_name} post
    def test_dn_create(self) -> None:
        response = client.post("/dn/dns.google.com")
        self.assertEqual(response.status_code, 200)
        self.assertIn("dn", response.json())
    
    def test_dn_create_already_exists(self) -> None:
        response = client.post("/dn/esiea.fr")
        self.assertEqual(response.status_code, 500)
    
    def test_dn_create_not_resolved(self) -> None:
        response = client.post("/dn/test")
        self.assertEqual(response.status_code, 500)

#/dn/{domain_name} get
    def test_dn_get(self) -> None:
        response = client.get("/dn/dns.google.com")
        self.assertEqual(response.status_code, 200)
        self.assertIn("dn", response.json())
        self.assertIn("dn_tags", response.json())
        self.assertIn("ip", response.json())
        self.assertIn("ip_tags", response.json())
        self.assertIn("owned", response.json())
        self.assertIn("followed", response.json())

#/dn/{domain_name} put

#/dn/{domain_name} delete

#/dn/{dn}/follow post

#/dn/{dn}/follow delete