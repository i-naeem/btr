"""
create_driver.py - Create the driver with common settings
"""
from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from configs import DRIVER_EXECUTABLE_PATH
from configs import LOADING_STRATEGY
from configs import CHROME_HEADLESS


def create_driver(ua, proxy) -> WebDriver:
    service = Service(executable_path=DRIVER_EXECUTABLE_PATH)
    options = ChromeOptions()

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

    prefs = {
        "webrtc.ip_handling_policy": "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled": False,
    }

    options.add_experimental_option('prefs', prefs)
    options.page_load_strategy = LOADING_STRATEGY
    options.add_argument(f"--user-agent={ua}")

    wire_options = {}

    if proxy.username and proxy.password:
        wire_options = {
            'proxy': {
                'http': proxy._proxy_url(),
                'https': proxy._proxy_url(),
                'no_proxy': 'localhost,127.0.0.1'
            }
        }

    driver = Chrome(
        service=service,
        options=options,
        headless=CHROME_HEADLESS,
        seleniumwire_options=wire_options,
        driver_executable_path=DRIVER_EXECUTABLE_PATH
    )

    driver.maximize_window()

    return driver
