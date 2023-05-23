import time
import utils
import random
import constants
import search


HOST = constants.HOSTS.get('MER_JOB')

START_URL = "https://google.com"  # HOST.get('start_url')
ANCHOR_SELECTOR = HOST.get('anchor_selector')
ANCHOR_SELECT_BY = HOST.get('anchor_select_by')


driver = search.duckduckgo("site:merjob.com", "merjob.com")


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
