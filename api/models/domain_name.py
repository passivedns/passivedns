import dns.rdatatype
import dns.resolver
from whois import whois
from datetime import datetime

from models.dns_records import *
from models.ip_address import IPAddress
from models.meta_node import Node
from db.database import get_db
from db.queries.dn_list import *
from db.queries.alert_list import *
from utils import timezone, config

DOMAIN_NAME_COLLECTION = "DomainName"


class DomainNameResolutionError(Exception):
    pass


class DomainNameFilterNotFound(Exception):
    pass


class DomainNameSortNotFound(Exception):
    pass


ALERT_FILTERS = {
    "domainName": ALERT_LIST_FILTER_DN,
    "dnTags": ALERT_LIST_FILTER_DN_TAGS,
    "ipTags": ALERT_LIST_FILTER_IP_TAG,
}

ALERT_SORT = {
    "domainName": ALERT_LIST_SORT_DN,
    "lastIpAddress": ALERT_LIST_SORT_LAST_IP,
    "currentIpAddress": ALERT_LIST_SORT_CURRENT_IP,
}


DOMAIN_NAME_FILTERS = {
    "domainName": DOMAIN_NAME_LIST_FILTER_DN,
    "dnTags": DOMAIN_NAME_LIST_FILTER_DN_TAG,
    "ipTags": DOMAIN_NAME_LIST_FILTER_IP_TAG,
}

DOMAIN_NAME_SORT = {
    "domainName": DOMAIN_NAME_LIST_SORT_DN,
    "ipAddress": DOMAIN_NAME_LIST_SORT_IP,
    "lastIpChange": DOMAIN_NAME_LIST_SORT_CHANGE
}


class DomainName(Node):
    def __init__(self, **dn_json):
        """
        The DomainName constructor
        :param dn_json: the JSON parsed object as returned by `self.json()`
        """
        self.domain_name = dn_json['key']
        super().__init__(DOMAIN_NAME_COLLECTION, self.domain_name)

        self.records = dn_json['records']
        self.registrar = dn_json['registrar']
        self.created_at = datetime.fromisoformat(dn_json['created_at'])

    def json(self):
        """
        Serialize the DomainName
        :return: JSON
        """
        return dict(
            _key=self.domain_name,
            records=self.records,
            registrar=self.registrar,
            created_at=self.created_at.isoformat()
        )

    def resolve(self) -> IPAddress:
        """
        Update the domain name DNS records and get the linked IP address
        :return: None if no resolution found, the resolved IP address else
        """
        self.records = DomainName._extract_records(self.domain_name)
        for r in self.records:
            if r['type'] == dns.rdatatype.A.name:
                return r['address']

        # in case resolution fails (no A record found), returns None
        return None

    @staticmethod
    def new(domain_name: str):
        """
        Build a new DomainName object, and extract its DNS records
        :param domain_name: the domain name to resolve
        :return: a new DomainName object
        """
        records = DomainName._extract_records(domain_name)
        # whois_infos = whois(domain_name)
        # registrar = whois_infos.registrar
        # if registrar is None:
        registrar = ""

        created_at = timezone.get_current_datetime(config.g.TIMEZONE)
        return DomainName(key=domain_name, records=records, registrar=registrar, created_at=created_at)

    @staticmethod
    def exists(domain_name: str):
        """
        Check if a DomainName exists in DB
        :param domain_name: the domain name
        :return: True if exists, False else
        """
        return DomainName._exists(
            DOMAIN_NAME_COLLECTION, domain_name
        )

    @staticmethod
    def full_list():
        """
        Get the full list of DomainName stored
        :return: a list of domain name strings
        """
        # returns a list of domain_names string
        dn_list = DomainName._list(DOMAIN_NAME_COLLECTION)
        return [dn['_key'] for dn in dn_list]

    @staticmethod
    def list(username, input_filter, input_filter_by, owned_filter: bool, followed_filter: bool, sort_by, limit: int):
        """
        List the DomainName, filter, sort, and limit the
        results (all in the AQL query)
        :param followed_filter: filter the followed DN only
        :param owned_filter: filter the owned DN only
        :param username: the User name
        :param input_filter: the text to use for filter
        :param input_filter_by: domainName, dnTags, ipTags
        :param sort_by: domainName, ipAddress, lastIpChange
        :param limit: the maximum count of results to return
        :return: the processed list of results of DomainName
        """

        query = DOMAIN_NAME_LIST_QUERY
        bind_vars = dict()
        bind_vars['username'] = username
        if input_filter != '':
            # unhandled filter type
            if input_filter_by not in DOMAIN_NAME_FILTERS.keys():
                raise DomainNameFilterNotFound

            filter_query = DOMAIN_NAME_FILTERS[input_filter_by]
            query += filter_query
            bind_vars['filter'] = input_filter

        # unhandled sort type
        if sort_by not in DOMAIN_NAME_SORT.keys():
            raise DomainNameSortNotFound

        sort_query = DOMAIN_NAME_SORT[sort_by]
        query += sort_query

        if owned_filter and followed_filter:
            query += DOMAIN_NAME_LIST_FILTER_FOLLOWED_OWNED

        elif followed_filter:
            query += DOMAIN_NAME_LIST_FILTER_FOLLOWED

        elif owned_filter:
            query += DOMAIN_NAME_LIST_FILTER_OWNED

        query += DOMAIN_NAME_LIST_RETURN
        bind_vars['limit'] = limit

        session = get_db()
        dn_list = session.exec_aql(
            query,
            bind_vars=bind_vars
        )

        return dn_list

    @staticmethod
    def list_recent_changes(username: str, days: int, input_filter, input_filter_by, sort_by, limit: int):
        """
        List the DomainName from which the IP recently changed
        :param username: the User name
        :param days: the maximum days delay of IP change
        :param input_filter: the text to use for filter
        :param input_filter_by: domainName, dnTags, ipTags
        :param sort_by: domainName, lastIpAddress, currentIpAddress
        :param limit: the maximum count of results to return
        :return: the processed list of results of DomainName
        """
        bind_vars = dict()
        query = ALERT_LIST_QUERY
        bind_vars['username'] = username

        if input_filter != '':
            if input_filter_by not in ALERT_FILTERS.keys():
                raise DomainNameFilterNotFound

            filter_query = ALERT_FILTERS[input_filter_by]
            query += filter_query
            bind_vars['filter'] = input_filter

        if sort_by not in ALERT_SORT.keys():
            raise DomainNameSortNotFound

        sort_query = ALERT_SORT[sort_by]
        query += sort_query

        query += ALERT_LIST_RETURN
        bind_vars['limit'] = limit
        bind_vars['days'] = days

        session = get_db()
        alert_list = session.exec_aql(query, bind_vars=bind_vars)
        return alert_list

    @staticmethod
    def get(domain_name):
        """
        Get an existing DomainName from DB
        :param domain_name: the domain name
        :return: an existing DomainName object
        """
        dn = DomainName._get(DOMAIN_NAME_COLLECTION, domain_name)
        return DomainName(
            key=dn['_key'],
            records=dn['records'],
            registrar=dn['registrar'],
            created_at=dn['created_at']
        )

    @staticmethod
    def _extract_records(domain_name):
        """
        Get the domain name DNS records
        :param domain_name: the domain name
        :return: the parsed DNS records
        """
        out = []
        records = []
        query_types = ['A', 'NS', 'SOA', 'MX', 'TXT', 'AAAA']
        for query_type in query_types:
            try:
                records.extend(list(
                    dns.resolver.resolve(domain_name, query_type)
                ))
            except dns.exception.DNSException:
                continue

        for r in records:
            out.append(
                DomainName._parse_rdatatype_record(r).json()
            )

        return out

    @staticmethod
    def _parse_rdatatype_record(r):
        """
        Parse a single DNS record
        :param r: the extracted record
        :return: the parsed record
        """
        if r.rdtype == dns.rdatatype.A:
            return DnsRecordA(r)

        elif r.rdtype == dns.rdatatype.NS:
            return DnsRecordNS(r)

        elif r.rdtype == dns.rdatatype.SOA:
            return DnsRecordSOA(r)

        elif r.rdtype == dns.rdatatype.MX:
            return DnsRecordMX(r)

        elif r.rdtype == dns.rdatatype.TXT:
            return DnsRecordTXT(r)

        elif r.rdtype == dns.rdatatype.AAAA:
            return DnsRecordAAAA(r)

        else:
            return DnsRecordOther(r)
