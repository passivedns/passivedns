from unittest import TestCase
from unittest.mock import MagicMock

from models.ip_address import IPAddress, IPAddressLocationError
from db.database import ObjectNotFound

from utils import config
config.init_config()

address = "51.83.46.84"


class TestIpAddress(TestCase):
    def test_init(self):
        i = IPAddress.new(address)
        self.assertEqual(i.address, address)
        self.assertEqual(i.location.organization, 'OVH')

    ##def test_init_location_error(self):
    ##    with self.assertRaises(IPAddressLocationError):
    ##        IPAddress.new("stuff")

    def test_json(self):
        self.maxDiff = None
        i = IPAddress.new(address)
        expected_json = {
            '_key': '51.83.46.84',
            'location': {
                'country': 'France',
                'country_code': 'FR',
                'region': 'HDF',
                'region_name': 'Hauts-de-France',
                'city': 'Roubaix',
                'zip_code': '59100',
                'latitude': 50.6917,
                'longitude': 3.20157,
                'timezone': 'Europe/Paris',
                'ISP': 'OVH SAS',
                'organization': 'OVH',
                'AS': 'AS16276 OVH SAS'
            }
        }
        self.assertEqual(i.json(), expected_json)

    def test_exists_true(self):
        IPAddress._exists = MagicMock(return_value=True)
        self.assertTrue(IPAddress.exists(address))

    def test_exists_false(self):
        IPAddress._exists = MagicMock(return_value=False)
        self.assertFalse(IPAddress.exists(address))

    def test_get(self):
        j = {
            "_id": "id",
            "_key": "key",
            "_rev": "rev",
            'address': '51.83.46.84',
            'location': {
                'country': 'France',
                'country_code': 'FR',
                'region': 'HDF',
                'region_name': 'Hauts-de-France',
                'city': 'Roubaix',
                'zip_code': '59100',
                'latitude': 50.6917,
                'longitude': 3.20157,
                'timezone': 'Europe/Paris',
                'ISP': 'OVH SAS',
                'organization': 'OVH',
                'AS': 'AS16276 OVH SAS'
            }
        }
        IPAddress._get = MagicMock(return_value=j)
        i = IPAddress.get(address)
        self.assertEqual(i.address, j['_key'])
        self.assertEqual(i.location.zip_code, j['location']['zip_code'])

    def test_get_error(self):
        IPAddress._get = MagicMock(side_effect=ObjectNotFound('not found'))
        with self.assertRaises(ObjectNotFound):
            IPAddress.get("stuff")




