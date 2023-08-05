import requests
from .user import User

class Entry():
    def __init__(self):
        self.url = "https://playentry.org/api/"

    def fetch_user_by_username(self, username: str) -> User:
        endpoint = self.url + f'getUserByUsername/{username}'
        resp = requests.get(endpoint)
        resp.raise_for_status()
        result = resp.json()
        user = User(data=result)
        return user
        
class AsyncEntry():
    def __init__(self):
        self.url = "https://playentry.org/api/"