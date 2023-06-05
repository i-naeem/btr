from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from typing import Dict, List, Tuple
import constants
import logging
import random
import errno
import json
import time
import os


def create_file(file_path: str) -> None:
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(file_path, "w") as f:
        f.write("")


def use_logger(should_stream: bool = True,
               level: str = logging.DEBUG,
               logger_name: str = f"btr__{int(time.time())}.log"
               ) -> logging.Logger:

    LOGGER = "BTR"
    logger = logging.getLogger(LOGGER)

    logs_file = f"./logs/{logger_name}"

    create_file(logs_file)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhandler = logging.FileHandler(filename=logs_file, mode='a')

    fhandler.setFormatter(formatter)
    logger.setLevel(level=level)

    logger.addHandler(fhandler)

    if should_stream:
        shandler = logging.StreamHandler()
        logger.addHandler(shandler)

    return logger


def use_driver(
        port: str = None,
        server: str = None,
        protocol: str = None,
        username: str = None,
        password: str = None,
) -> WebDriver:
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
    options.add_argument("--blink-settings=imagesEnabled=false")
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
    if username and password and protocol and server and port:
        proxy = f"{protocol}://{username}:{password}@{server}:{port}"
        print(f'Using proxy: {server}:{port}', )
        wire_options = {
            'proxy': {
                'http': proxy,
                'https': proxy,
                'no_proxy': 'localhost,127.0.0.1'
            }
        }

    driver = Chrome(service=service, options=options, seleniumwire_options=wire_options)
    driver.maximize_window()

    return driver


def scroll_down(driver: WebDriver, pause: float = 0.5) -> None:
    scroll_height = driver.execute_script('return document.body.scrollHeight')
    scroll_speed = 300  # Pixels
    scrolled_pixel = scroll_speed
    while scrolled_pixel < scroll_height:
        driver.execute_script('return window.scrollTo(0, arguments[0])', scrolled_pixel)
        scrolled_pixel = scrolled_pixel + scroll_speed
        time.sleep(pause)


def scroll_up(driver: WebDriver, pause: float = 0.5) -> None:
    scroll_y = driver.execute_script('return window.scrollY')
    scroll_speed = 200

    while scroll_y > 0:
        driver.execute_script('return window.scrollBy(0, -arguments[0])', scroll_speed)
        scroll_y = scroll_y - scroll_speed
        time.sleep(pause)


def scroll_to_element(driver: WebDriver, element: WebElement) -> None:
    driver.execute_script("""
function scrollToElement(element) {
  const rect = element.getBoundingClientRect();
  const scrollY = window.scrollY || window.pageYOffset;
  const scrollX = window.scrollX || window.pageXOffset;
  const scrollTargetY = scrollY + rect.top - window.innerHeight / 2;
  const scrollTargetX = scrollX + rect.left - window.innerWidth / 2;
  const duration = Math.floor(Math.random() * (2500 - 1000) + 1000)
  const easing = function(t) {
    return t * (2 - t);
  };
  let start;

  if (!scrollTargetY && !scrollTargetX) {
    return;
  }

  window.requestAnimationFrame(function step(timestamp) {
    if (!start) {
      start = timestamp;
    }

    const time = timestamp - start;
    let percent = Math.min(time / duration, 1);
    percent = easing(percent);

    window.scrollTo(
      scrollX + (scrollTargetX - scrollX) * percent,
      scrollY + (scrollTargetY - scrollY) * percent
    );

    if (time < duration) {
      window.requestAnimationFrame(step);
    }
  });
}


element = arguments[0]
scrollToElement(element);""",
                          element)


def use_proxies(max: int = 1) -> List[Dict[str, str]]:
    if os.path.exists(constants.PROXIES_FILE_PATH):
        # [{"protocol": "http", "server": "192.192.32.1", "port": "8888"},...]
        with open(constants.PROXIES_FILE_PATH, "r") as f:
            return random.sample(json.load(f), k=max)
    else:
        raise FileNotFoundError


def find_by_selectors(
        driver: WebDriver,
        selectors: List[Tuple[str, str]],
        wait_time: int = 10) -> List[WebElement]:
    logger = logging.getLogger(constants.LOGGER)

    wait = WebDriverWait(driver, wait_time)

    all_elements = []
    for selector in selectors:
        try:
            elements = wait.until(EC.presence_of_all_elements_located(selector))
            all_elements.extend(elements)
        except TimeoutException as e:
            logger.warn(f'No Elements ({selector = })')

    print(f'FOUND ELMENTS: [{len(all_elements)}]')
    return all_elements
