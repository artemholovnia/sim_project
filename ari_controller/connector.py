import requests, websocket
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse

class WebSocketConnector():
    def __init__(self, url):
        self.url = url

    def get_or_create_connection(self):
        parsed_url = urlparse(self.url)
        print(parsed_url)
        return parsed_url

