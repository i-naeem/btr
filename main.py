from selenium.webdriver.common.action_chains import ActionChains
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urljoin, urlparse
import random


DRIVER_PATH = "./files/chromedriver.exe"
START_URL = "https://merjob.com"

visited_urls = set()


def normalize_url(url):
    return str(urljoin(url, urlparse(url).path))


def find_anchors(driver):
    anchors_list = []

    anchors = driver.find_elements(by=By.CSS_SELECTOR, value=".wp-block-latest-posts__post-title")
    for anchor in anchors:
        href = normalize_url(anchor.get_attribute('href'))
        if href.find('category') == -1:
            if href not in map(lambda item: item.get('href'), anchors_list) and href not in visited_urls:
                anchors_list.append({"href": href, "el": anchor})

    return anchors_list


service = Service(executable_path=DRIVER_PATH)
chrome_options = ChromeOptions()

driver = Chrome(service=service, options=chrome_options)
driver.maximize_window()

driver.get(START_URL)
content_area = driver.find_element(by=By.ID, value="main")

for i in range(15):
    driver.implicitly_wait(3)
    anchors = find_anchors(driver)
    anchor = random.choice(anchors)
    element = anchor.get('el')
    driver.execute_script('arguments[0].scrollIntoView(true);', element)
    element.click()

    print(f'VIEW: [{anchor.get("href")}]')

input('Press any key to qiut')
driver.quit()
