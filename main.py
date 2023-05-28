import env
import utils
import random
from Bot import Bot
from models import Selector
from selenium.webdriver.common.by import By
from search_controller import SearchController
from selenium.webdriver.chrome.service import Service
from undetected_chromedriver import Chrome, ChromeOptions

search_engines = [
    {
        "start_url": "https://bing.com",
        "selector": Selector(by=By.CSS_SELECTOR, value="h2 > a"),
    },
    {
        "start_url": "https://duckduckgo.com",
        "selector": Selector(by=By.CSS_SELECTOR, value="h2 > .result-title-a"),
    }
]


def main(proxy):
    service = Service(executable_path=env.CHROME_EXECUTABLE_PATH)
    chrome_options = utils.get_chrome_options(proxy)
    chrome_options.page_load_strategy = 'eager'
    driver = Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    search_engine = random.choice(search_engines)
    driver.get(search_engine.get("start_url"))

    controller = SearchController(
        driver=driver, search_result_selectors=search_engine.get("selector")
    )

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
        max_views=4
    )

    bot.start()
