import validators
import requests
from utils import config
from utils.timezone import to_current_timezone
from datetime import datetime
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
            out = self.get_api(self.api.name)(response.json())
            return out
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
    
    def get_api(self,api_name:str):
        __MAPPING ={
            VIRUSTOTAL_API:self.__formatVT,
            ALIENVAULT_API: self.__formatAV
        }

        assert api_name in __MAPPING
        
        return __MAPPING[api_name]
    
    #VirusTotal formatting
    def __formatVT(self, response):
        datas = response["data"]

        out = []

        for data in datas:
            date = datetime.fromtimestamp(data["attributes"]["date"])

            date = to_current_timezone(config.g.TIMEZONE, date)

            out.append(
                {
                    "domain_name":data["attributes"]["host_name"],
                    "ip_address":data["attributes"]["ip_address"],
                    "first_updated_at": date,
                    "last_updated_at": date,
                }
            )
        
        return out

    #AlienVault formatting
    def __formatAV(self, response):
        datas = response["passive_dns"]

        out = []

        for data in datas:
            first = datetime.fromisoformat(data["first"])
            last = datetime.fromisoformat(data["last"])

            first = to_current_timezone(config.g.TIMEZONE, first)
            last = to_current_timezone(config.g.TIMEZONE, last)

            out.append(
                {
                    "domain_name":data["hostname"],
                    "ip_address":data["address"],
                    "first_updated_at": first,
                    "last_updated_at": last,
                }
            )

        return out
