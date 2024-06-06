
import requests

class APIIntegration(object):
    """
    The base class for a API integration
    """

    def __init__(self, api_name, api_url, api_key, username):
        self.api_name = api_name
        self.api_url = api_url
        self.api_key = api_key
        self.username = username
        

    #def json(self): #todo

    #    return self
    
    def get(self, uri, params={}):
        url =  self.api_url + uri
        headers = {
            "accept": "application/json", 
            "X-Apikey": self.api_key
        }

        response = requests.get(
            url, headers=headers, params=params
        )
        response.raise_for_status()

        return response.json()

class VirusTotalAPI(APIIntegration):
    def __init__(self, user_key, username):
        super().__init__("VirusTotal", "https://www.virustotal.com/api/v3/", user_key, username)
    

    def getDomain(domain):
        uri = "domains/"+domain+"/resolutions"
        return super().get(uri)
    
    def getIP(ip):
        uri = "ip_addresses/"+ip+"/resolutions"
        return super().get(uri)

class AlienVaultAPI(APIIntegration):
    def __init__(self, user_key, username):
        super().__init__("OTX AlienVault", "https://otx.alienvault.com/api/v1/", user_key, username)
    
    
    def getDomain(domain):
        uri = "/indicators/domain/"+domain+"/passive_dns"
        return super().get(uri)

    def getIP(ip):
        uri = "/indicators/IPv4/"+ip+"/passive_dns"
        return super().get(uri)