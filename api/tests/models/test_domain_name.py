from unittest import TestCase
from unittest.mock import MagicMock

from models.domain_name import DomainName, DomainNameResolutionError
from db.database import ObjectNotFound

domain_name = "dadard.fr"


class TestDomainName(TestCase):
    def test_init(self):
        d = DomainName.new(domain_name)
        self.assertEqual(d.domain_name, domain_name)

    def test_resolve(self):
        d = DomainName.new(domain_name)
        ip = d.resolve()

        expected_ip_address = "216.239.34.21"
        self.assertEqual(ip, expected_ip_address)

    def test_resolve_exception(self):
        d = DomainName.new("stuff")
        ip = d.resolve()
        self.assertEqual(ip, None)

    def test_exists_true(self):
        DomainName._exists = MagicMock(return_value=True)
        self.assertTrue(DomainName.exists(domain_name))

    def test_exists_false(self):
        DomainName._exists = MagicMock(return_value=False)
        self.assertFalse(DomainName.exists(domain_name))

    def test_get(self):
        j = {
            "_key": domain_name,
            "records": [
                {"type": "A", "address": "address"}
            ],
            "registrar": "registrar",
            "created_at":"2024-04-23T16:42:11.583591+02:00"
        }
        DomainName._get = MagicMock(return_value=j)
        d = DomainName.get(domain_name)
        self.assertEqual(d.domain_name, domain_name)
        self.assertEqual(d.records[0]['address'], "address")

    def test_get_error(self):
        DomainName._get = MagicMock(side_effect=ObjectNotFound('not found'))
        with self.assertRaises(ObjectNotFound):
            DomainName.get("stuff")
