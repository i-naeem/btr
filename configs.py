"""
configs.py - Configuration settings for the bot.
"""
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

load_dotenv()


MAX_TABS = 3
MAX_TRAVERSES = 2
ADVERTISEMENT_PAUSE_TIME = 60

HEADLESS = False


DRIVER_EXECUTABLE_PATH = os.environ.get('DRIVER_EXECUTABLE_PATH', "./assets/chromedriver.exe")
PROXIES_FILE_PATH = os.environ.get("PROXIES_FILE_PATH", "./assets/proxies.json")
PROXIES_USERNAME = os.environ.get("PROXIES_USERNAME", None)
PROXIES_PASSWORD = os.environ.get("PROXIES_PASSWORD", None)


ADVERTISEMENT_SELECTORS = [
    (By.CSS_SELECTOR, 'a[href*="adclick"]'),
    (By.CSS_SELECTOR, 'a[href*="doubleclick"]'),
    (By.CSS_SELECTOR, 'a[href*="googleadservice"]'),
]
