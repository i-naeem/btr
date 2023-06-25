"""
create_driver.py - Create the driver with common settings
"""
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver


def create_driver() -> WebDriver:
    service = Service(executable_path="")
    chrome_options = ChromeOptions()

    driver = Chrome(service=service, options=chrome_options)

    return driver
