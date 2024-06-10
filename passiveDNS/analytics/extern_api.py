
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

class ExternAPI:
    """
    The base class for external apis
    """

    def __init__(self, api:APIIntegration, api_key:str):
        self.api = api
        self.api_key = api_key
        
    
    def __get(self, uri, method, params={}, data={}, json={}):
        url =  self.api.url + uri
        headers = {
            "accept": "application/json", 
            "X-Apikey": self.api_key
        }
        if method == 'GET':
            response = requests.get(
                url, headers=headers, params=params
            )
        elif method == 'POST':
            response = requests.post(
                url, headers=headers, data=data, json=json
            )
        else :
            raise MethodException(method)
        
        response.raise_for_status()

        return response.json()
    
    
    def requestDomain(self, domain:DomainName):
        #check if domain is valid
        if not validators.domain(domain.domain_name):
            raise FormatException
        
        uri = self.api.domain_uri % domain.domain_name
        return self.__get(uri)

    def requestIP(self, ip:IPAddress):
        #check if ip is valid
        if not validators.ipv4(ip.address):
            raise FormatException
        
        uri = self.api.ip_uri % ip.address
        return self.__get(uri)