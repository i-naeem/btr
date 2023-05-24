import time
import utils
import random
import constants

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException

KEY_DELAY_RANGE = (0.1, 0.2)
service = Service(executable_path=constants.DRIVER_PATH)
chrome_options = ChromeOptions()

chrome_options.add_argument("--no-sandbox")
driver = Chrome(service=service, options=chrome_options)
driver.start_session()
driver.maximize_window()


def google(keywords: str, host: str):
    start_url = "https://google.com"
    driver.get(start_url)
    time.sleep(1)
    searchbar = driver.find_element(by=By.TAG_NAME, value="textarea")

    for key in keywords:
        searchbar.send_keys(key)
        time.sleep(random.uniform(*KEY_DELAY_RANGE))

    searchbar.send_keys(Keys.ENTER)
    time.sleep(1)

    items = []
    search_items = driver.find_elements(by=By.XPATH, value="//a[h3]")

    for item in search_items:

        href = item.get_attribute('href')
        if href.find(host) != -1:
            items.append(item.find_element(by=By.TAG_NAME, value="h3"))

    random_item = random.choice(items)

    random_item.click()
    time.sleep(1)

    utils.scroll_page(driver)

    _root = driver.find_element(by=By.CSS_SELECTOR, value='a[rel=home]')
    _root.click()
    time.sleep(1)
    return driver


def bing(keywords: str, host: str):
    start_url = "https://bing.com"
    driver.get(start_url)
    time.sleep(1)
    searchbar = driver.find_element(by=By.ID, value="sb_form_q")

    for key in keywords:
        searchbar.send_keys(key)
        time.sleep(random.uniform(*KEY_DELAY_RANGE))

    searchbar.send_keys(Keys.ENTER)

    items = []
    search_items = driver.find_elements(by=By.CSS_SELECTOR, value=".b_algo h2")

    for item in search_items:
        anchor = item.find_element(by=By.TAG_NAME, value="a")
        href = anchor.get_attribute('href')
        if href.find(host) != -1:
            items.append(item)

    random_item = random.choice(items)
    random_item.click()
    time.sleep(1)

    utils.scroll_page(driver)

    _root = driver.find_element(by=By.CSS_SELECTOR, value='a[rel=home]')
    _root.click()
    time.sleep(1)
    return driver


def duckduckgo(keywords: str, host: str):
    start_url = "https://duckduckgo.com"
    driver.get(start_url)

    searchbar = None

    try:
        searchbar = driver.find_element(by=By.ID, value="search_form_input_homepage")
    except NoSuchElementException:
        searchbar = driver.find_element(by=By.ID, value="searchbox_input")

    if searchbar is None:
        raise NoSuchElementException('Search bar is not located with both ids')

    for key in keywords:
        searchbar.send_keys(key)
        time.sleep(random.uniform(*KEY_DELAY_RANGE))

    searchbar.send_keys(Keys.ENTER)
    time.sleep(1)

    items = []
    search_items = driver.find_elements(by=By.CSS_SELECTOR, value="article h2")

    for item in search_items:
        anchor = item.find_element(by=By.TAG_NAME, value="a")
        href = anchor.get_attribute('href')
        if href.find(host) != -1:
            items.append(item)

    random_item = random.choice(items)
    random_item.click()
    time.sleep(1)

    utils.scroll_page(driver)

    _root = driver.find_element(by=By.CSS_SELECTOR, value='a[rel=home]')
    _root.click()
    time.sleep(1)

    return driver
