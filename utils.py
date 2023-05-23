"""
utils.py - utility functions that will help in project.

random_ua(): Returns a random user agent string.
normalize_url(url): Normalize url by removing extra parameters from the url.
"""

import time
import random
from constants import USER_AGENTS
from urllib.parse import urljoin, urlparse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains


def random_ua() -> str:
    """
    Returns a random user agent string.

    Returns:
        str: A random user agent.
    """

    return random.choice(USER_AGENTS)


def normalize_url(url: str) -> str:
    """
    Normalize the url by removing extra parameters from the url such search params etc.

    Args:
        url (str): The raw url scrapped form the page.

    Returns:
        str: Normalized URL.


    """

    path = urlparse(url).path
    normalized_url = urljoin(url, path)

    return str(normalized_url)


def scroll_page(driver: WebDriver, speed: float = 1) -> None:
    scroll_height = driver.execute_script("return document.body.scrollHeight")

    # Create an instance of ActionChains
    actions = ActionChains(driver)

    # Perform the scroll action until the end of the page is reached
    while driver.execute_script("return window.pageYOffset + window.innerHeight") < scroll_height:
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(speed)
