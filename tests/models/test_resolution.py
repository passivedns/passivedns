from unittest import TestCase
from unittest.mock import MagicMock

from passiveDNS.models.resolution import Resolution
from passiveDNS.models.domain_name import DOMAIN_NAME_COLLECTION
from passiveDNS.models.ip_address import IP_ADDRESS_COLLECTION
from passiveDNS.db.database import ObjectNotFound
from passiveDNS.db.database import get_db
from passiveDNS.utils import config

config.init_config()

domain_name = "dadard.fr"
ip_address = "51.83.46.84"

from_id = f"{DOMAIN_NAME_COLLECTION}/{domain_name}"
to_id = f"{IP_ADDRESS_COLLECTION}/{ip_address}"

example_res = {
    "_from": from_id,
    "_to": to_id,
    "domain_name": domain_name,
    "ip_address": ip_address,
    "last_updated_at": "2021-03-06T13:14:38.301500",
    "first_updated_at": "2021-03-06T13:14:38.301500",
    "resolver": "PassiveDNS",
}

example_res_list = [example_res]


class TestResolution(TestCase):
    def setUp(self):
        self.db = get_db()
        self.db.connect()
        self.db.clear()

    def tearDown(self):
        self.db.clear()

    def test_init(self):
        d = Resolution.new(domain_name, ip_address, "PassiveDNS")
        self.assertEqual(d._from, from_id)
        self.assertEqual(d._to, to_id)

    def test_exists_true(self):
        Resolution._exists = MagicMock(return_value=True)
        self.assertTrue(Resolution.exists(domain_name, ip_address))

    def test_exists_false(self):
        Resolution._exists = MagicMock(return_value=False)
        self.assertFalse(Resolution.exists(domain_name, ip_address))

    def test_get(self):
        Resolution._get = MagicMock(return_value=example_res)
        r = Resolution.get(domain_name, ip_address)
        self.assertEqual(r._from, from_id)
        self.assertEqual(r._to, to_id)
        self.assertEqual(r.last_updated_at.isoformat(), example_res["last_updated_at"])

    def test_get_error(self):
        Resolution._get = MagicMock(side_effect=ObjectNotFound("not found"))
        with self.assertRaises(ObjectNotFound):
            Resolution.get("stuff", "stuff")

    def test_list_from_ip(self):
        Resolution._list_from = MagicMock(return_value=example_res_list)
        r_list = Resolution.list_from_ip(ip_address)
        self.assertEqual(len(r_list), len(example_res_list))
        self.assertEqual(
            r_list[0].last_updated_at.isoformat(),
            example_res_list[0]["last_updated_at"],
        )

    def test_list_from_domain(self):
        Resolution._list_to = MagicMock(return_value=example_res_list)
        r_list = Resolution.list_from_domain(domain_name)
        self.assertEqual(len(r_list), len(example_res_list))
        self.assertEqual(
            r_list[0].last_updated_at.isoformat(),
            example_res_list[0]["last_updated_at"],
        )
