from datetime import datetime, date

from passiveDNS.models.meta_edge import Edge
from passiveDNS.models.domain_name import DOMAIN_NAME_COLLECTION, DomainNameResolutionError
from passiveDNS.models.ip_address import IP_ADDRESS_COLLECTION
from passiveDNS.utils import timezone, config

RESOLUTION_COLLECTION = "DomainNameResolution"


class Resolution(Edge):
    def __init__(self, **resolution_json):
        """
        The Resolution constructor
        :param resolution_json: the JSON parsed object as returned by `self.json()`
        """
        super().__init__(
            RESOLUTION_COLLECTION, resolution_json["_from"], resolution_json["_to"]
        )
        self.domain_name = resolution_json["domain_name"]
        self.ip_address = resolution_json["ip_address"]
        self.resolver = resolution_json["resolver"]
        self.last_updated_at = datetime.fromisoformat(
            resolution_json["last_updated_at"]
        )
        self.first_updated_at = datetime.fromisoformat(
            resolution_json["first_updated_at"]
        )

    def json(self):
        """
        Serialize the Resolution
        :return: JSON
        """
        return {
            "_from": self._from,
            "_to": self._to,
            "domain_name": self.domain_name,
            "ip_address": self.ip_address,
            "resolver": self.resolver,
            "last_updated_at": self.last_updated_at.isoformat(),
            "first_updated_at": self.first_updated_at.isoformat(),
        }

    def update(self):
        """
        Set the last updated date to now and last resolver, and save in DB
        :return:
        """
        self.last_updated_at = timezone.get_current_datetime(config.g.TIMEZONE)
        self._update(dict(last_updated_at=self.last_updated_at, resolver=self.resolver))

    @staticmethod
    def new(
        domain_name: str,
        ip_address: str,
        resolver: str,
        last_updated: date = None,
        first_updated: date = None,
    ):
        """
        Build a new Resolution object
        :param domain_name: the domain name to link
        :param ip_address: the IP address to link
        :return: the  build Resolution
        """
        from_id = Resolution._get_id(DOMAIN_NAME_COLLECTION, domain_name)
        to_id = Resolution._get_id(IP_ADDRESS_COLLECTION, ip_address)

        if last_updated is None:
            last = timezone.get_current_datetime(config.g.TIMEZONE)
        else:
            last = last_updated

        if first_updated is None:
            first = timezone.get_current_datetime(config.g.TIMEZONE)
        else:
            first = first_updated

        return Resolution(
            _from=from_id,
            _to=to_id,
            domain_name=domain_name,
            ip_address=ip_address,
            resolver=resolver,
            last_updated_at=last,
            first_updated_at=first,
        )

    @staticmethod
    def exists(domain_name: str, ip_address: str):
        """
        Check if a Resolution exists between a domain name and an IP address
        :param domain_name: the domain name
        :param ip_address: the IP address
        :return: True if exists, False else
        """
        return Resolution._exists(
            RESOLUTION_COLLECTION,
            DOMAIN_NAME_COLLECTION,
            domain_name,
            IP_ADDRESS_COLLECTION,
            ip_address,
        )

    @staticmethod
    def get(domain_name: str, ip_address: str):
        """
        Get an existing Resolution object from DB
        :param domain_name: the domain name
        :param ip_address: the IP address
        :return: the existing Resolution object
        """
        resolution_json = Resolution._get(
            RESOLUTION_COLLECTION,
            DOMAIN_NAME_COLLECTION,
            domain_name,
            IP_ADDRESS_COLLECTION,
            ip_address,
        )

        return Resolution(**resolution_json)

    @staticmethod
    def list_from_ip(ip_address: str):
        """
        List all the Resolution connected to a specific IP address
        :param ip_address: the IP address
        :return: the list of Resolution connected
        """
        edges = Resolution._list_from(
            RESOLUTION_COLLECTION, IP_ADDRESS_COLLECTION, ip_address
        )
        return [Resolution(**e) for e in edges]

    @staticmethod
    def list_from_domain(domain_name: str):
        """
        List all the Resolution connected to a specific domain name
        :param domain_name: the domain name
        :return: the list of Resolution connected
        """
        edges = Resolution._list_to(
            RESOLUTION_COLLECTION, DOMAIN_NAME_COLLECTION, domain_name
        )
        return [Resolution(**e) for e in edges]

    @staticmethod
    def get_current_from_domain(domain_name: str):
        """
        Get the last updated Resolution for a specific domain name
        :param domain_name: the domain name
        :return: the filtered Resolution
        :raise: DomainNameResolutionError if no resolution found
        """
        res_list = Resolution.list_from_domain(domain_name)
        if len(res_list) == 0:
            raise DomainNameResolutionError(f"no resolution found for {domain_name}")

        current = res_list[0]
        for r in res_list:
            if r.last_updated_at > current.last_updated_at:
                current = r

        return current
