import unittest
from fastapi.testclient import TestClient

from db.database import get_db
from models.user import User
from models.tag import Tag
from models.tag_dn_ip import TagDnIP
from models.domain_name import DomainName, DOMAIN_NAME_COLLECTION
from main import app

client = TestClient(app)


class TagTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()

        cls.user1 = User.new(
            username="TestUser1", password="user1", email="user1@test.com"
        )
        cls.user1.insert()

        cls.tag2 = Tag.new("testTag2")
        cls.tag2.insert()

        cls.tag3 = Tag.new("testTag3")
        cls.tag3.insert()

        cls.tag4 = Tag.new("testTag4")
        cls.tag4.insert()

        cls.tag5 = Tag.new("testTag5")
        cls.tag5.insert()

        cls.dn4 = DomainName.new("dns.google.com")
        cls.dn4.insert()

        cls.tagdn5 = TagDnIP.new("testTag2", "dns.google.com", DOMAIN_NAME_COLLECTION)
        cls.tagdn5.insert()
        cls.tagdn6 = TagDnIP.new("testTag5", "dns.google.com", DOMAIN_NAME_COLLECTION)
        cls.tagdn6.insert()

        client.post("/token", json={"identity": "TestUser1", "password": "user1"})

    @classmethod
    def tearDownClass(cls) -> None:
        client.get("/logout")
        cls.user1.delete()
        cls.tag2.delete()
        Tag.get("testTag1").delete()

        cls.tag4.delete()
        cls.dn4.delete()
        cls.tag5.delete()

        cls.tagdn5.delete()
        TagDnIP.get("testTag4", "dns.google.com", DOMAIN_NAME_COLLECTION).delete()

    # tag

    # /tag/{name} post
    def test_create_tag(self) -> None:
        response = client.post("/tag/testTag1")
        self.assertEqual(response.status_code, 200)

    def test_create_tag_already_exists(self) -> None:
        response = client.post("/tag/testTag2")
        self.assertEqual(response.status_code, 500)

    # /tag/{name} delete
    def test_delete_tag(self) -> None:
        response = client.delete("/tag/testTag3")
        self.assertEqual(response.status_code, 200)

    def test_delete_tag_not_found(self) -> None:
        response = client.delete("/tag/test")
        self.assertEqual(response.status_code, 404)

    # /tag get
    def test_get_tag(self) -> None:
        response = client.get("/tag")
        self.assertEqual(response.status_code, 200)

    # tag_dn_ip

    # /tag_dn_ip post
    def test_create_tag_dn_ip(self) -> None:
        response = client.post(
            "/tag_dn_ip",
            params={
                "tag": "testTag4",
                "object": "dns.google.com",
                "type": DOMAIN_NAME_COLLECTION,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("tag_link", response.json())

    def test_create_tag_dn_ip_already_exists(self) -> None:
        response = client.post(
            "/tag_dn_ip",
            params={
                "tag": "testTag2",
                "object": "dns.google.com",
                "type": DOMAIN_NAME_COLLECTION,
            },
        )
        self.assertEqual(response.status_code, 500)

    def test_create_tag_dn_ip_tag_not_found(self) -> None:
        response = client.post(
            "/tag_dn_ip",
            params={
                "tag": "test",
                "object": "dns.google.com",
                "type": DOMAIN_NAME_COLLECTION,
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_create_tag_dn_ip_invalid_type(self) -> None:
        response = client.post(
            "/tag_dn_ip",
            params={"tag": "testTag4", "object": "dns.google.com", "type": "this"},
        )
        self.assertEqual(response.status_code, 400)

    def test_create_tag_dn_ip_target_not_found(self) -> None:
        response = client.post(
            "/tag_dn_ip",
            params={
                "tag": "testTag4",
                "object": "example.com",
                "type": DOMAIN_NAME_COLLECTION,
            },
        )
        self.assertEqual(response.status_code, 404)

    # /tag_dn_ip/{tag}/{object}/{type} delete
    def test_delete_tag_dn_ip(self) -> None:
        response = client.delete(
            f"/tag_dn_ip/testTag5/dns.google.com/{DOMAIN_NAME_COLLECTION}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("tag_link", response.json())

    def test_delete_tag_dn_ip_not_found(self) -> None:
        response = client.delete(
            f"/tag_dn_ip/test/dns.google.com/{DOMAIN_NAME_COLLECTION}"
        )
        self.assertEqual(response.status_code, 404)

    # /tag_dn_ip/list/from
    def test_get_tag_list(self) -> None:
        response = client.get(
            "/tag_dn_ip/list/from",
            params={"object": "dns.google.com", "type": DOMAIN_NAME_COLLECTION},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("tag_link_list", response.json())
