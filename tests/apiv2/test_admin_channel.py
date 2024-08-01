import unittest
from fastapi.testclient import TestClient

from passiveDNS.db.database import get_db
from passiveDNS.models.user import User
from passiveDNS.models.channel import Channel
from passiveDNS.webserver import app

client = TestClient(app)


class AdminChannelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()
        cls.db.clear()
        cls.db.connect()
        cls.admin1 = User(
            _key="TestAdmin1",
            hashed_password=User._hash_password("admin1"),
            role="admin",
            api_keys={},
        )
        cls.admin1.insert()

        cls.channel1 = Channel.new(
            "channelTest1",
            "redis",
            {
                "host": "test",
                "port": "test",
                "db": "test",
            },
        )
        cls.channel1.insert()

        cls.channel2 = Channel.new(
            "channelTest2",
            "redis",
            {
                "host": "test2",
                "port": "test2",
                "db": "test2",
            },
        )
        cls.channel2.insert()

        client.post(
            "/apiv2/token", json={"identity": "TestAdmin1", "password": "admin1"}
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.clear()

    # /admin/channels get
    def test_admin_channel_list(self) -> None:
        response = client.get("/apiv2/admin/channels")
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel_list", response.json())

    # /admin/channels/{name} post
    def test_admin_create_channel(self) -> None:
        response = client.post(
            "/apiv2/admin/channels/test1",
            json={
                "type": "redis",
                "infos": {
                    "host": "test",
                    "port": "test",
                    "db": "test",
                },
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel", response.json())

    def test_admin_create_channel_already_exists(self) -> None:
        response = client.post(
            "/apiv2/admin/channels/_default",
            json={
                "type": "redis",
                "infos": {
                    "host": "test",
                    "port": "test",
                    "db": "test",
                },
            },
        )
        self.assertEqual(response.status_code, 500)

    def test_admin_create_channel_parsing_error(self) -> None:
        response = client.post(
            "/apiv2/admin/channels/test3",
            json={"type": "redis", "infos": {"host": "test", "port": "test"}},
        )
        self.assertEqual(response.status_code, 500)

    def test_admin_create_channel_invalid_type(self) -> None:
        response = client.post(
            "/apiv2/admin/channels/test4",
            json={
                "type": "test",
                "infos": {
                    "host": "test",
                    "port": "test",
                    "db": "test",
                },
            },
        )
        self.assertEqual(response.status_code, 400)

    # /admin/channels/{name} get
    def test_admin_get_channel(self) -> None:
        response = client.get("/apiv2/admin/channels/_default")
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel", response.json())

    def test_admin_get_channel_not_found(self) -> None:
        response = client.get("/apiv2/admin/channels/none")
        self.assertEqual(response.status_code, 404)

    # /admin/channels/{name} put
    def test_admin_update_channel(self) -> None:
        response = client.put(
            "/apiv2/admin/channels/channelTest1",
            json={
                "type": "redis",
                "infos": {
                    "host": "changed",
                    "port": "changed",
                    "db": "changed",
                },
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel", response.json())

    def test_admin_update_channel_not_found(self) -> None:
        response = client.put(
            "/apiv2/admin/channels/test5",
            json={
                "type": "redis",
                "infos": {
                    "host": "changed",
                    "port": "changed",
                    "db": "changed",
                },
            },
        )
        self.assertEqual(response.status_code, 404)

    # /admin/channels/{name} delete
    def test_admin_delete_channel(self) -> None:
        response = client.delete("/apiv2/admin/channels/channelTest2")
        self.assertEqual(response.status_code, 200)
        self.assertIn("channel", response.json())

    def test_admin_delete_channel_default(self) -> None:
        response = client.delete("/apiv2/admin/channels/_default")
        self.assertEqual(response.status_code, 403)

    def test_admin_delete_channel_not_found(self) -> None:
        response = client.delete("/apiv2/admin/channels/test6")
        self.assertEqual(response.status_code, 404)
