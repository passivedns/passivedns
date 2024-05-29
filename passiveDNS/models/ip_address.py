import logging
import time

import requests

from models.meta_node import Node

IP_ADDRESS_COLLECTION = "IPAddress"


class IPAddressLocationError(Exception):
    pass


class IPAddressLocation(object):
    # https://ip-api.status.io/ https://ip-api.com/
    _base_url = "http://ip-api.com/json/"
    _json_fields = [
        "country",
        "countryCode",
        "region",
        "regionName",
        "city",
        "zip",
        "lat",
        "lon",
        "timezone",
        "isp",
        "org",
        "as",
    ]
    _attributes = [
        "country",
        "country_code",
        "region",
        "region_name",
        "city",
        "zip_code",
        "latitude",
        "longitude",
        "timezone",
        "ISP",
        "organization",
        "AS",
    ]

    def __init__(self, **ip_location_json):
        """
        The IPAddressLocation constructor
        :param ip_location_json: the JSON parsed, object as returned by `self.json()`
        """
        for f in self._attributes:
            self.__setattr__(f, ip_location_json[f])
        return

    @staticmethod
    def new(address):
        """
        Build a new IPAddressLocation object from an address
        :param address: the IP address
        :return: the parsed location
        """

        resp = requests.get(IPAddressLocation._base_url + address)
        if resp.headers["X-Rl"] == "0":
            timeout = float(resp.headers["X-Ttl"])
            print(f"IP API rate limit reached - waiting for {timeout}")
            time.sleep(timeout)
            resp = requests.get(IPAddressLocation._base_url + address)

        if resp.status_code != 200 or resp.json()["status"] != "success":
            # couldn't retrieve the location from an IP address
            default = ""
            return IPAddressLocation(
                country=default,
                country_code=default,
                region=default,
                region_name=default,
                city=default,
                zip_code=default,
                latitude=default,
                longitude=default,
                timezone=default,
                ISP=default,
                organization=default,
                AS=default,
            )

        j = {}
        location_json = resp.json()
        for i in range(len(IPAddressLocation._attributes)):
            j[IPAddressLocation._attributes[i]] = location_json[
                IPAddressLocation._json_fields[i]
            ]

        return IPAddressLocation(**j)

    def json(self) -> dict:
        """
        Serialize the IPAddressLocation
        :return: JSON
        """
        out = dict()
        for a in self._attributes:
            out[a] = self.__getattribute__(a)

        return out


class IPAddress(Node):
    def __init__(self, **ip_json):
        """
        The IPAddress constructor
        :param ip_json: the JSON parsed object as returned by `self.json()`
        """
        self.address = ip_json["key"]
        super().__init__(IP_ADDRESS_COLLECTION, self.address)

        if "location" in ip_json:
            self.location = IPAddressLocation(**ip_json["location"])

    def json(self):
        """
        Serialize the IPAddress
        :return: JSON
        """
        js_dict = {"_key": self.address, "location": self.location.json()}
        return js_dict

    @staticmethod
    def new(address):
        """
        Build a new IPAddress from an IP address
        :param address: the IP address
        :return: a new IPAddress
        """
        location = IPAddressLocation.new(address)
        return IPAddress(key=address, location=location.json())

    @staticmethod
    def exists(address: str):
        """
        Check if an IPAddress exists in DB
        :param address: the IP address
        :return: True if exists, False else
        """
        return IPAddress._exists(IP_ADDRESS_COLLECTION, address)

    @staticmethod
    def list():
        """
        List the stored IPAddress
        :return: the IPAddress object list
        """
        ip_list = IPAddress._list(IP_ADDRESS_COLLECTION)
        return [IPAddress(key=ip["_key"], location=ip["location"]) for ip in ip_list]

    @staticmethod
    def get(address: str):
        """
        Get an existing IPAddress from DB
        :param address: the IP address
        :return: the existing IPAddress object
        """
        ip = IPAddress._get(IP_ADDRESS_COLLECTION, address)

        return IPAddress(key=ip["_key"], location=ip["location"])
