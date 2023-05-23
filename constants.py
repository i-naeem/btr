from selenium.webdriver.common.by import By

DRIVER_PATH = "./files/chromedriver.exe"

USER_AGENTS = [
    "Mozila",
    "Chrome",
    "Edge"
]

HOSTS = {
    "MER_JOB": {
        "start_url": "https://merjob.com",
        "anchor_selector": ".entry-title a",
        "anchor_select_by": By.CSS_SELECTOR,
    }
}
