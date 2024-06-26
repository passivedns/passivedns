import unittest
from fastapi.testclient import TestClient

from passiveDNS.db.database import get_db
from passiveDNS.models.user import User
from passiveDNS.models.user_channel import UserChannel
from passiveDNS.models.channel import Channel
from passiveDNS.webserver import app

client = TestClient(app)


class UserChannelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()
        cls.db.clear()

        cls.user1 = User.new(
            username="TestUser1", password="user1", email="user1@test.com"
        )
        cls.user1.insert()

        cls.channelUser1 = UserChannel.new("TestUser1", "_default", "user1@test.com")
        cls.channelUser1.insert()

        # Test already verified
        cls.channel2 = Channel.new(
            "channelTest1",
            "email",
            {
                "smtp_host": "test",
                "smtp_port": "test",
                "sender_email": "test",
                "sender_password": "test",
            },
        )
        cls.channel2.insert()

        cls.channelUser2 = UserChannel.new(
            "TestUser1", "channelTest1", "user1@test.com"
        )
        cls.channelUser2.update(verified=True)
        cls.channelUser2.insert()

        # Test wrong token
        cls.channel3 = Channel.new(
            "channelTest2",
            "email",
            {
                "smtp_host": "test",
                "smtp_port": "test",
                "sender_email": "test",
                "sender_password": "test",
            },
        )
        cls.channel3.insert()

        cls.channelUser3 = UserChannel.new(
            "TestUser1", "channelTest2", "user1@test.com"
        )
        cls.channelUser3.insert()

        # Test delete
        cls.channel4 = Channel.new(
            "channelTest3",
            "email",
            {
                "smtp_host": "test",
                "smtp_port": "test",
                "sender_email": "test",
                "sender_password": "test",
            },
        )
        cls.channel4.insert()

        cls.channelUser4 = UserChannel.new(
            "TestUser1", "channelTest3", "user1@test.com"
        )
        cls.channelUser4.insert()

        # User login
        client.post("/token", json={"identity": "TestUser1", "password": "user1"})

    @classmethod
    def tearDownClass(cls) -> None:
        client.get("/logout")
        cls.db.clear()

    # /channels get
    def test_channels_get(self) -> None:
        response = client.get("/channels")
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel_list", response.json())
        self.assertIn("_key", response.json()["channel_list"][0])
        self.assertEqual("_default", response.json()["channel_list"][0]["_key"])

    # /channels/{name} get
    def test_channel_get_by_name(self) -> None:
        response = client.get("/channels/_default")
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel", response.json())
        self.assertIn("_key", response.json()["channel"])
        self.assertEqual("_default", response.json()["channel"]["_key"])

    def test_channel_get_by_name_not_found(self) -> None:
        response = client.get("/channels/test")
        self.assertEqual(response.status_code, 404)

    # /user/channels get
    def test_user_channels_get(self) -> None:
        response = client.get("/user/channels")
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel_list", response.json())
        self.assertIn("user_channel", response.json()["channel_list"][0])
        self.assertIn("channel", response.json()["channel_list"][0])

    # /users/channels/{name} get
    def test_user_channel_get_by_name(self) -> None:
        response = client.get("/user/channels/_default")
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_channel", response.json())
        self.assertIn("channel_name", response.json()["user_channel"])
        self.assertEqual("_default", response.json()["user_channel"]["channel_name"])

    def test_user_channel_get_by_name_not_found(self) -> None:
        response = client.get("/user/channels/test")
        self.assertEqual(response.status_code, 404)

    # /users/channels/{name} post : mail sending so manual testing

    # /users/channels/{name} put
    def test_user_channel_verify(self) -> None:
        response = client.put(
            "/user/channels/_default", json={"token": self.channelUser1.token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_channel", response.json())

    def test_user_channel_verify_not_found(self) -> None:
        response = client.put(
            "/user/channels/test", json={"token": self.channelUser1.token}
        )
        self.assertEqual(response.status_code, 404)

    def test_user_channel_verify_already_verified(self) -> None:
        response = client.put(
            "/user/channels/channelTest1", json={"token": self.channelUser1.token}
        )
        self.assertEqual(response.status_code, 500)

    def test_user_channel_verify_invalid_token(self) -> None:
        response = client.put("/user/channels/channelTest2", json={"token": "test"})
        self.assertEqual(response.status_code, 500)

    # /users/channels/{name} delete
    def test_user_channel_delete(self) -> None:
        response = client.delete("/user/channels/channelTest3")
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_channel", response.json())

    def test_user_channel_delete_default(self) -> None:
        response = client.delete("/user/channels/_default")
        self.assertEqual(response.status_code, 500)

    def test_user_channel_delete_not_found(self) -> None:
        response = client.delete("/user/channels/test")
        self.assertEqual(response.status_code, 404)


# /users/channels/{name}/test get : mail sending so manual testing
