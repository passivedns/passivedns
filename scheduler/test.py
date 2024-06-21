import requests

r = requests.post(
    "http://api:8080/token", json={"identity": "sched_1", "password": "sched_1"}
)
access_token = r.json()["access_token"]
print(access_token)
headers = {"Authorization": f"Bearer {access_token}"}
r = requests.get("http://api:8080/scheduler/alerts", headers=headers)
print(r.json())
