import requests
from pydantic import BaseModel

class LoginError(Exception):
    pass


class RequestError(Exception):
    pass


class ApiClient(BaseModel):
    host: str
    username: str
    password: str
    token: str = ""

    def login(self): 
        r = requests.post(f"{self.host}/token", json={"identity": self.username, "password": self.password})
        if r.status_code != 200:
            raise LoginError(r.status_code)
        self.token = r.json()["access_token"]

    def dn_update(self, domain_name) -> int:
        r = requests.put(f"{self.host}/scheduler/dn/{domain_name}", headers={"Authorization": f"Bearer {self.token}"})
        return r.status_code

    def dn_list(self):
        r = requests.get(f"{self.host}/scheduler/alerts", headers={"Authorization": f"Bearer {self.token}"})
        if r.status_code != 200:
            raise RequestError(r.status_code)

        return r.json()["dn_list"]
