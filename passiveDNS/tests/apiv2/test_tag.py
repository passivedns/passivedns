import unittest
from fastapi.testclient import TestClient

from db.database import get_db
from models.user import User
from models.tag import Tag
from models.tag_dn_ip import TagDnIP
from main import app

client = TestClient(app)

class TagTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()

        cls.user1 = User.new(username="TestUser1", password="user1", email="user1@test.com")
        cls.user1.insert()

        cls.tag2 = Tag.new("testTag2")
        cls.tag2.insert()

        cls.tag3 = Tag.new("testTag3")
        cls.tag3.insert()

        client.post("/token", json={"identity":"TestUser1", "password":"user1"})

    @classmethod
    def tearDownClass(cls) -> None:
        client.get("/logout")
        cls.user1.delete()
        cls.tag2.delete()
        Tag.get("testTag1").delete()
    
    #tag

#/tag/{name} post
    def test_create_tag(self) -> None:
        response = client.post("/tag/testTag1")
        self.assertEqual(response.status_code, 200)
    
    def test_create_tag_already_exists(self) -> None:
        response = client.post("/tag/testTag2")
        self.assertEqual(response.status_code, 500)

#/tag/{name} delete
    def test_delete_tag(self) -> None:
        response = client.delete("/tag/testTag3")
        self.assertEqual(response.status_code, 200)
    
    def test_delete_tag_not_found(self) -> None:
        response = client.delete("/tag/test")
        self.assertEqual(response.status_code, 404)

#/tag get
    def test_get_tag(self) -> None:
        response = client.get("/tag")
        self.assertEqual(response.status_code, 200)

    #tag_dn_ip

#/tag_dn_ip post

#/tag_dn_ip/{tag}/{object}/{type} delete

#/tag_dn_ip/list/from