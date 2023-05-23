import time
import utils
import random
import constants
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from undetected_chromedriver import Chrome, ChromeOptions


HOST = constants.HOSTS.get('MER_JOB')

START_URL = "https://google.com"  # HOST.get('start_url')
ANCHOR_SELECTOR = HOST.get('anchor_selector')
ANCHOR_SELECT_BY = HOST.get('anchor_select_by')


def search():
    service = Service(executable_path=constants.DRIVER_PATH)
    chrome_options = ChromeOptions()

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--incoginito")

    driver = Chrome(service=service, options=chrome_options)
    driver.get(START_URL)
    driver.maximize_window()

    time.sleep(1)
    searchbar = driver.find_element(By.TAG_NAME, "textarea")
    searchbar.send_keys("site:merjob.com")
    searchbar.send_keys(Keys.ENTER)
    time.sleep(1)
    time.sleep(1)

    anchors = driver.find_elements(by=By.CSS_SELECTOR, value=".g  a")
    host = None
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if href.find("merjob.com") != -1:
            host = anchor.find_element(by=By.TAG_NAME, value='h3')
            break

    if host:
        time.sleep(1)
        host.click()
    else:
        print("Your site was not found in the links")
        driver.quit()

    return driver


driver = search()


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
