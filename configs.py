"""
configs.py - Configuration settings for the bot.
"""
from selenium.webdriver.common.by import By

# Bot
MAX_TABS = 3
MAX_TRAVERSES = 2
ADVERTISEMENT_PAUSE_TIME = 60


# Driver
DRIVER_EXECUTABLE_PATH = "./assets/chromedriver.exe"
HEADLESS = False


ADVERTISEMENT_SELECTORS = [
    (By.CSS_SELECTOR, 'a[href*="adclick"]'),
    (By.CSS_SELECTOR, 'a[href*="doubleclick"]'),
    (By.CSS_SELECTOR, 'a[href*="googleadservice"]'),
]
