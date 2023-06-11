from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
import logging


def use_driver() -> WebDriver:
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
    # options.add_argument("--blink-settings=imagesEnabled=false")
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

    wire_options = {}

    driver = Chrome(service=service, options=options, seleniumwire_options=wire_options)
    driver.maximize_window()

    return driver


def find_by_selectors(driver, selectors, timeout=2, max_element=5):
    wait = WebDriverWait(driver, timeout)

    all_elements = []
    for selector in selectors:
        if len(all_elements) > max_element:
            return all_elements
        try:
            elements = wait.until(EC.presence_of_all_elements_located(selector))
            all_elements.extend(elements)
        except TimeoutException as e:
            logging.warning(f'TIMEOUT: [{selector}]')
            logging.exception(e)

    return all_elements
