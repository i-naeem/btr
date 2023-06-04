from selenium.webdriver.common.by import By
LOGGER = "BTR"
PROXIES_FILE_PATH = "./assets/proxies.json"

DEFAULT_AD_SELECTORS = [
    (By.CSS_SELECTOR, 'a[href*="adclick"]'),
    (By.CSS_SELECTOR, 'a[href*="doubleclick"]'),
    (By.CSS_SELECTOR, 'a[href*="googleadservice"]'),
]
