# The proxies are authenticated by IP Address so it will not work on someone else pc
# Get the trail version from WebShare.io and use your own proxies instead of these
from selenium.webdriver.chrome.service import Service
from undetected_chromedriver import Chrome
from dataclasses import dataclass
import random
import utils
import env


@dataclass
class Proxy:
    protocol: str
    server: str
    port: str


PROXIES = [
    Proxy(protocol="socks5", server="185.199.229.156", port="7492"),
    Proxy(protocol="socks5", server="185.199.228.220", port="7300"),
    Proxy(protocol="socks5", server="185.199.231.45", port="8382"),
    Proxy(protocol="socks5", server="188.74.210.207", port="6286"),
    Proxy(protocol="socks5", server="188.74.183.10", port="8279"),
    Proxy(protocol="socks5", server="188.74.210.21", port="6100"),
    Proxy(protocol="socks5", server="45.155.68.129", port="8133"),
    Proxy(protocol="socks5", server="154.95.36.199", port="6893"),
    Proxy(protocol="socks5", server="2.56.119.93", port="5074"),
    Proxy(protocol="socks5", server="45.94.47.66", port="8110")
]


if __name__ == '__main__':
    print("Testing Proxy")
    service = Service(executable_path=env.CHROME_EXECUTABLE_PATH)
    options = utils.get_chrome_options(proxy=random.choice(PROXIES))
    driver = Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(5)

    driver.get("https://browserleaks.com/ip")
    input("Press enter to quit")
