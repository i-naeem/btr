from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service


def use_driver(proxy=None):
    service = Service(executable_path="./assets/chromedriver.exe")
    options = ChromeOptions()

    prefs = {
        "webrtc.ip_handling_policy": "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled": False,
    }
    options.add_experimental_option('prefs', prefs)

    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-seccomp-filter-sandbox")
    options.add_argument("--disable-impl-side-painting")
    options.add_argument('--disable-plugins-discovery')
    options.add_argument("--allow-http-screen-capture")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-popup-blocking')
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-logging')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')

    if proxy:
        options.add_argument(
            f'--proxy-server={proxy.protocol}://{proxy.server}:{proxy.port}'
        )

    driver = Chrome(service=service, options=options)

    return driver
