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
    Proxy(protocol="socks5", server="2.56.119.93", port="5074"),
]