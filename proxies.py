# WebShare.io jude.10@mailtouiq.com:123password123
# The proxies are authenticated by IP Address so it will not work on someone else pc
# Get the trail version from WebShare.io and use your own proxies instead of these 
from dataclasses import dataclass


@dataclass
class Proxy:
    protocol: str;
    server: str;
    port: str;

PROXIES = [
    Proxy(protocol="http", server="2.56.119.93", port="5074"),
    Proxy(protocol="http", server="45.94.47.66", port="8110"),
    Proxy(protocol="http", server="188.74.183.10", port="8279"),
    Proxy(protocol="http", server="188.74.210.21", port="6100"),
    Proxy(protocol="http", server="45.155.68.129", port="8133"),
    Proxy(protocol="http", server="154.95.36.199", port="6893"),
    Proxy(protocol="http", server="185.199.231.45", port="8382"),
    Proxy(protocol="http", server="188.74.210.207", port="6286"),
    Proxy(protocol="http", server="185.199.229.156", port="7492"),
    Proxy(protocol="http", server="185.199.228.220", port="7300"),
]