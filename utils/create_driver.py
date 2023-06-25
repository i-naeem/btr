"""
create_driver.py - Create the driver with common settings
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome, ChromeOptions
from configs import DRIVER_EXECUTABLE_PATH


def create_driver() -> WebDriver:
    service = Service(executable_path=DRIVER_EXECUTABLE_PATH)
    chrome_options = ChromeOptions()

    driver = Chrome(
        service=service,
        options=chrome_options,
        # driver_executable_path=DRIVER_EXECUTABLE_PATH
    )

    return driver
