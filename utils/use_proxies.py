from configs import PROXIES_FILE_PATH
from configs import PROXIES_PASSWORD
from configs import PROXIES_USERNAME
from dataclasses import dataclass
from typing import List
import random
import os


@dataclass
class Proxy:
    port: int
    server: str
    protocol: str
    username: str
    password: str

    def _proxy_url(self):
        return f"{self.protocol}://{self.username}:{self.password}@{self.server}:{self.port}"


def use_proxies(proxies_list: List, start: int = 1, max_proxies: int = 5) -> List[Proxy]:
    proxies = proxies_list[start: max_proxies + 1]
    return [Proxy(username=PROXIES_USERNAME, password=PROXIES_PASSWORD, **p) for p in proxies]
