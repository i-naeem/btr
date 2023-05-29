from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service


def use_driver():
    service = Service(executable_path="./assets/chromedriver.exe")
    options = ChromeOptions()
    driver = Chrome(service=service, options=options)

    return driver
