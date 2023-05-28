from undetected_chromedriver import ChromeOptions
from fake_useragent import UserAgent
from models import Proxy
import logging

logger = logging.getLogger(name="BTR")

logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('./logs/btr.log', 'a'))
logger.addHandler(logging.StreamHandler())


def get_chrome_options(proxy: Proxy = None, ua: UserAgent = None):
    prefs = {"webrtc.ip_handling_policy": "disable_non_proxied_udp",
             "webrtc.multiple_routes_enabled": False,
             "webrtc.nonproxied_udp_enabled": False, }

    ua = ua if ua else UserAgent().random
    options = ChromeOptions()
    options.add_argument('--disable-logging')
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    options.add_argument(f'--user-agent={ua}')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-plugins-discovery')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    options.add_argument("--disable-seccomp-filter-sandbox")
    options.add_argument("--allow-http-screen-capture")
    options.add_argument("--disable-impl-side-painting")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    options.add_experimental_option('prefs', prefs)

    if proxy:
        options.add_argument(
            f'--proxy-server={proxy.protocol}://{proxy.server}:{proxy.port}'
        )

    return options
