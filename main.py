import time
import utils
import random
import constants
from selenium.webdriver.chrome.service import Service
from undetected_chromedriver import Chrome, ChromeOptions


HOST = constants.HOSTS.get('MER_JOB')

START_URL = HOST.get('start_url')
ANCHOR_SELECTOR = HOST.get('anchor_selector')
ANCHOR_SELECT_BY = HOST.get('anchor_select_by')


service = Service(executable_path=constants.DRIVER_PATH)
chrome_options = ChromeOptions()

chrome_options.add_argument("--no-sandbox")

# Add custom headers
headers = {
    'Referer': 'https://www.facebook.com/'
}
chrome_options.add_argument(f"--headers={headers}")

driver = Chrome(service=service, options=chrome_options)
driver.maximize_window()

driver.get(START_URL)


for i in range(5):
    utils.scroll_page(driver)
    anchors = driver.find_elements(ANCHOR_SELECT_BY, ANCHOR_SELECTOR)
    anchor = random.choice(anchors)
    href = anchor.get_attribute("href")
    driver.execute_script('arguments[0].scrollIntoView()', anchor)
    anchor.click()
    time.sleep(2)
    utils.scroll_page(driver)
    time.sleep(1)
    driver.back()


input('Press any key to qiut')
driver.quit()
