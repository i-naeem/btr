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
items = controller.search(q="site:yourfabulouslives.com")

bot = Bot(
    driver=driver,
    available_pages=items,
    selectors=[Selector(By.CSS_SELECTOR, 'h2 > a')],
    max_tabs=3,
    max_views=8
)

bot.start()
