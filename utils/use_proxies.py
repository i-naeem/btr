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


def use_proxies(start: int = 1, max_proxies: int = 5) -> List[Proxy]:
    if os.path.exists(PROXIES_FILE_PATH):
        proxies = []
        with open(PROXIES_FILE_PATH, "r") as p_file:
            counter = 0
            for line in p_file:
                counter = counter + 1
                if counter < start:
                    continue
                if counter == max_proxies:
                    break

                port, server, protocol = line.strip().split(',')
                proxies.append(
                    Proxy(port=port,
                          server=server,
                          protocol=protocol,
                          username=PROXIES_USERNAME,
                          password=PROXIES_PASSWORD,
                          )
                )

        random.shuffle(proxies)
        return proxies
    else:
        raise FileNotFoundError
