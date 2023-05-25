from selenium.webdriver.common.by import By

DRIVER_PATH = "./files/chromedriver.exe"


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"

HOSTS = {
    "MER_JOB": {
        "start_url": "https://merjob.com",
        "anchor_selector": ".entry-title a",
        "anchor_select_by": By.CSS_SELECTOR,
    }
}
