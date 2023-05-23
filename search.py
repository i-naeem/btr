import time
import utils
import random
import constants
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from undetected_chromedriver import Chrome, ChromeOptions

service = Service(executable_path=constants.DRIVER_PATH)
chrome_options = ChromeOptions()

chrome_options.add_argument("--no-sandbox")
driver = Chrome(service=service, options=chrome_options)


def bing(keywords: str, host: str):
    start_url = "https://google.com"
    driver.get(start_url)
    driver.maximize_window()
    pass


def google(keywords: str, host: str):
    start_url = "https://bing.com"
    driver.get(start_url)
    driver.maximize_window()

    pass


def duckduckgo(keywords: str, host: str):
    start_url = "https://duckduckgo.com"
    driver.get(start_url)
    driver.maximize_window()
    pass
