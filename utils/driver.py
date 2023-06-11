from selenium.webdriver.chrome.service import Service
from seleniumwire.undetected_chromedriver import ChromeOptions, Chrome


def use_driver():
    s = Service(executable_path='./assets/chromedriver.exe')
    o = ChromeOptions()
    so = dict()

    return Chrome(service=s, options=o, seleniumwire_options=so)
