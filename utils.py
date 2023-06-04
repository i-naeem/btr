from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from typing import Dict, List
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
        proxy_protocol: str = None,
        proxy_server: str = None,
        proxy_port: str = None,
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

    if proxy_protocol and proxy_server and proxy_port:
        options.add_argument(
            f'--proxy-server={proxy_protocol}://{proxy_server}:{proxy_port}'
        )

    driver = Chrome(service=service, options=options)
    driver.maximize_window()

    return driver


def scroll_down(driver: WebDriver, pause: float = 0.5) -> None:
    actions = ActionChains(driver)
    while True:
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(pause)

        is_end = driver.execute_script(
            "return window.innerHeight + window.pageYOffset >= document.body.scrollHeight"
        )

        # Check if reached the end of the page
        if is_end:
            break


def scroll_up(driver: WebDriver, pause: float = 0.5) -> None:
    actions = ActionChains(driver)
    while True:
        actions.send_keys(Keys.PAGE_UP).perform()
        time.sleep(pause)  # Adjust the sleep time as needed
        # Check if reached the top of the page
        if driver.execute_script("return window.pageYOffset <= 0"):
            break


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
