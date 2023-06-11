from dataclasses import dataclass
from typing import List
import random
import json
import os


PROXIES_FILE_PATH = "./assets/proxies.json"


@dataclass
class Proxy:
    port: int
    server: str
    protocol: str
    username: str
    password: str

    def _proxy_url(self):
        return f"{self.protocol}://{self.username}:{self.password}@{self.server}:{self.port}"


def use_proxies(max: int = 1) -> List[Proxy]:
    pwd = os.environ.get('PROXY_PASSWORD')
    un = os.environ.get('PROXY_USERNAME')

    if os.path.exists(PROXIES_FILE_PATH):
        # [{"protocol": "http", "server": "192.192.32.1", "port": "8888"},...]
        with open(PROXIES_FILE_PATH, "r") as f:
            proxies = json.load(f)
            random.shuffle(proxies)
            return [Proxy(password=pwd, username=un, **p) for p in random.sample(proxies, k=max)]
    else:
        raise FileNotFoundError
