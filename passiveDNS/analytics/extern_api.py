
import requests
from models.api_integration import APIIntegration
from models.domain_name import DomainName
from models.ip_address import IPAddress

class ExternAPI:
    """
    The base class for external apis
    """

    def __init__(self, api:APIIntegration, api_key:str):
        self.api = api
        self.api_key = api_key
        
    
    def __get(self, uri, params={}):
        url =  self.api.url + uri
        headers = {
            "accept": "application/json", 
            "X-Apikey": self.api_key
        }

        response = requests.get( #method to check
            url, headers=headers, params=params
        )
        response.raise_for_status()

        return response.json()


class VirusTotalAPI(ExternAPI):
    def __init__(self, user_key:str):
        api = APIIntegration.get("VirusTotal")
        super().__init__(api, user_key)

    def getDomain(self, domain:DomainName):
        #check if domain
        uri = self.api.domain_uri % domain.domain_name
        return super().__get(uri)
        # ip_address - Attention aux ipv6
    
    def getIP(self, ip:IPAddress):
        #check if ip
        uri = self.api.ip_uri % ip.address
        return super().__get(uri)
        # host_name

class AlienVaultAPI(ExternAPI):
    def __init__(self, user_key:str):
        api = APIIntegration.get("OTX AlienVault")
        super().__init__(api, user_key)
    
    
    def getDomain(self, domain:DomainName):
        #check if domain
        uri = self.api.domain_uri % domain.domain_name
        return super().__get(uri)
        # address

    def getIP(self, ip:IPAddress):
        #check if ip
        uri = self.api.ip_uri % ip.address
        return super().__get(uri)
        # address