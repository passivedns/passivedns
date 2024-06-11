import validators
import requests
from models.api_integration import APIIntegration
from models.domain_name import DomainName
from models.ip_address import IPAddress

VIRUSTOTAL_API = "VirusTotal"
ALIENVAULT_API = "AlienVault"


class MethodException(Exception):
    pass


class FormatException(Exception):
    pass


class RequestException(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


class ExternAPI:
    """
    The base class for external apis
    """

    def __init__(self, api: APIIntegration, api_key: str):
        self.api = api
        self.api_key = api_key

    def __get(self, uri, method, params={}, data={}, json={}):
        url = self.api.base_url + uri
        headers = {"accept": "application/json", self.api.header: self.api_key}
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=data, json=json)
        else:
            raise MethodException(method)

        if response.status_code == 200:
            return response.json()
        raise RequestException(
            response.status_code, response.json()["error"]["message"]
        )

    def requestDomain(self, domain: DomainName):
        # check if domain is valid
        if not validators.domain(domain.domain_name):
            raise FormatException

        uri = self.api.domain_uri % domain.domain_name
        return self.__get(uri, self.api.domain_method)

    def requestIP(self, ip: IPAddress):
        # check if ip is valid
        if not validators.ipv4(ip.address):
            raise FormatException

        uri = self.api.ip_uri % ip.address
        return self.__get(uri, self.api.ip_method)

    def testRequest(self):
        uri = self.api.domain_uri % "dns.google.com"
        return self.__get(uri, self.api.domain_method)
