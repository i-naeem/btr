from dataclasses import dataclass
from selenium.webdriver.common.by import By


@dataclass
class Selector:
    by: By
    value: str


@dataclass
class Proxy:
    protocol: str
    server: str
    port: str
