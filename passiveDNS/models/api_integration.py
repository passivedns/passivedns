from models.meta_node import Node

APIINTEGRATION_COLLECTION = "APIIntegration"

class APIIntegration(Node):
    def __init__(self, **api_json):
        """
        The User constructor
        :param api_json: the JSON parsed object as returned by `self.json()`
        """
        self.name = api_json["_key"]
        super().__init__(APIINTEGRATION_COLLECTION, self.name)

        self.base_url = api_json["base_url"]
        self.header = api_json["header"]
        self.ip_method = api_json["ip"]["method"]
        self.ip_uri = api_json["ip"]["uri"]
        self.domain_method = api_json["domain"]["method"]
        self.domain_uri = api_json["domain"]["uri"]

    def json(self) -> dict:
        """
        Serialize the APIIntegration
        :return: JSON
        """
        return {
            "_key": self.name,
            "base_url": self.base_url,
            "header": self.header,
            "ip": {
                "method":self.ip_method,
                "uri": self.ip_uri,
            },
            "domain": {
                "method":self.domain_method,
                "uri": self.domain_uri,
            },
        }

    @staticmethod
    def get(name: str):
        """
        Get an existing APIIntegration from its name
        :param name: the API name
        :return: an existing APIIntegration
        """
        a = APIIntegration._get(APIINTEGRATION_COLLECTION, name)
        return APIIntegration(**a)