import random
from Bot import Bot
from models import Selector
from selenium.webdriver.common.by import By
from search_controller import SearchController
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from undetected_chromedriver import Chrome, ChromeOptions

service = Service(executable_path="./assets/chromedriver.exe")
options = ChromeOptions()
options.page_load_strategy = 'eager'
driver = Chrome(service=service, options=options)
driver.maximize_window()
driver.get('https://bing.com')

result_selectors = [
    Selector(by=By.CSS_SELECTOR, value="h2 > a")
]

controller = SearchController(driver=driver, search_result_selectors=result_selectors)
items = controller.search(q="site:merjob.com")

filtered_items = [
    item for item in items if item.get_attribute('href').find('merjob.com') != -1
]

bot = Bot(
    driver=driver,
    available_pages=filtered_items,
    selectors=[
        Selector(By.CLASS_NAME, 'wp-block-latest-posts__post-title'),
        Selector(By.CSS_SELECTOR, '.entry-title > a')
    ],
    max_tabs=5,
    max_views=50
)

bot.start()
