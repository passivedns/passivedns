import unittest
from fastapi.testclient import TestClient

from db.database import get_db
from models.user import User
from main import app

client = TestClient(app)

class UserChannelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()

        cls.user1 = User.new(username="TestUser1", password="user1", email="user1@test.com")
        cls.user1.insert()

        client.post("/token", json={"identity":"TestUser1", "password":"user1"})

    @classmethod
    def tearDownClass(cls) -> None:
        client.get("/logout")
        cls.user1.delete()
    
#/channels get
    def test_channels_get(self) -> None:
        response = client.get("/channels")
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel_list", response.json())
        self.assertIn("_key", response.json()["channel_list"][0])
        self.assertEqual("_default", response.json()["channel_list"][0]["_key"])

#/channels/{name} get
    def test_channel_get_by_name(self) -> None:
        response = client.get("/channels/_default")
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel", response.json())
        self.assertIn("_key", response.json()["channel"])
        self.assertEqual("_default", response.json()["channel"]["_key"])

    def test_channel_get_by_name_not_found(self) -> None:
        response = client.get("/channels/test")
        self.assertEqual(response.status_code, 404)

#/user/channels get

#/users/channels/{name} get

#/users/channels/{name} post

#/users/channels/{name} put

#/users/channels/{name} delete

#/users/channels/{name}/test get : mail sending so manual testing