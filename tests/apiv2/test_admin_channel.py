import unittest
from fastapi.testclient import TestClient

from db.database import get_db
from models.user import User
from models.channel import Channel
from passiveDNS.webserver import app

client = TestClient(app)


class AdminChannelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()
        cls.admin1 = User(
            _key="TestAdmin1",
            email="admin1@test.com",
            hashed_password=User._hash_password("admin1"),
            role="admin",
            api_keys={},
        )
        cls.admin1.insert()

        cls.channel1 = Channel.new(
            "channelTest1",
            "email",
            {
                "smtp_host": "test",
                "smtp_port": "test",
                "sender_email": "test",
                "sender_password": "test",
            },
        )
        cls.channel1.insert()

        cls.channel2 = Channel.new(
            "channelTest2",
            "email",
            {
                "smtp_host": "test2",
                "smtp_port": "test2",
                "sender_email": "test2",
                "sender_password": "test2",
            },
        )
        cls.channel2.insert()

        client.post("/token", json={"identity": "TestAdmin1", "password": "admin1"})

    @classmethod
    def tearDownClass(cls) -> None:
        client.get("/logout")
        cls.admin1.delete()
        cls.channel1.delete()
        Channel.get("test1").delete()

    # /admin/channels get
    def test_admin_channel_list(self) -> None:
        response = client.get("/admin/channels")
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel_list", response.json())

    # /admin/channels/{name} post
    def test_admin_create_channel(self) -> None:
        response = client.post(
            "/admin/channels/test1",
            json={
                "type": "email",
                "infos": {
                    "smtp_host": "test",
                    "smtp_port": "test",
                    "sender_email": "test",
                    "sender_password": "test",
                },
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel", response.json())

    def test_admin_create_channel_already_exists(self) -> None:
        response = client.post(
            "/admin/channels/_default",
            json={
                "type": "email",
                "infos": {
                    "smtp_host": "test",
                    "smtp_port": "test",
                    "sender_email": "test",
                    "sender_password": "test",
                },
            },
        )
        self.assertEqual(response.status_code, 500)

    def test_admin_create_channel_parsing_error(self) -> None:
        response = client.post(
            "/admin/channels/test3",
            json={"type": "email", "infos": {"smtp_host": "test", "smtp_port": "test"}},
        )
        self.assertEqual(response.status_code, 500)

    def test_admin_create_channel_invalid_type(self) -> None:
        response = client.post(
            "/admin/channels/test4",
            json={
                "type": "test",
                "infos": {
                    "smtp_host": "test",
                    "smtp_port": "test",
                    "sender_email": "test",
                    "sender_password": "test",
                },
            },
        )
        self.assertEqual(response.status_code, 400)

    # /admin/channels/{name} get
    def test_admin_get_channel(self) -> None:
        response = client.get("/admin/channels/_default")
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel", response.json())

    def test_admin_get_channel_not_found(self) -> None:
        response = client.get("/admin/channels/none")
        self.assertEqual(response.status_code, 404)

    # /admin/channels/{name} put
    def test_admin_update_channel(self) -> None:
        response = client.put(
            "/admin/channels/channelTest1",
            json={
                "type": "email",
                "infos": {
                    "smtp_host": "changed",
                    "smtp_port": "changed",
                    "sender_email": "changed",
                    "sender_password": "changed",
                },
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel", response.json())

    def test_admin_update_channel_not_found(self) -> None:
        response = client.put(
            "/admin/channels/test5",
            json={
                "type": "email",
                "infos": {
                    "smtp_host": "changed",
                    "smtp_port": "changed",
                    "sender_email": "changed",
                    "sender_password": "changed",
                },
            },
        )
        self.assertEqual(response.status_code, 404)

    # /admin/channels/{name} delete
    def test_admin_delete_channel(self) -> None:
        response = client.delete("/admin/channels/channelTest2")
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel", response.json())

    def test_admin_delete_channel_default(self) -> None:
        response = client.delete("/admin/channels/_default")
        self.assertEqual(response.status_code, 403)

    def test_admin_delete_channel_not_found(self) -> None:
        response = client.delete("/admin/channels/test6")
        self.assertEqual(response.status_code, 404)
