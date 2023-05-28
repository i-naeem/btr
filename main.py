import env
import utils
import random
from Bot import Bot
from models import Selector
from undetected_chromedriver import Chrome
from selenium.webdriver.common.by import By
from search_controller import SearchController
from selenium.webdriver.chrome.service import Service


search_engines = [
    # {
    #     "name": "Bing",
    #     "start_url": "https://bing.com",
    #     "selector": [Selector(by=By.CSS_SELECTOR, value="h2 > a")],
    # },
    {
        "name": "DuckDuckGo",
        "start_url": "https://duckduckgo.com",
        "selector": [Selector(by=By.CSS_SELECTOR, value="h2 > .result-title-a"),
                     Selector(by=By.CSS_SELECTOR, value=".result-link"),
                     Selector(by=By.TAG_NAME, value="a"),
                     ],
    }
]


def main(proxy=None, q=None, f=None):
    service = Service(executable_path=env.CHROME_EXECUTABLE_PATH)
    chrome_options = utils.get_chrome_options(proxy=proxy)
    # chrome_options.page_load_strategy = 'eager'

    utils.logger.info(f'{main.__name__}: Starting driver')

    driver = Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(20)

    search_engine = random.choice(search_engines)

    utils.logger.info(f"{main.__name__}: Select {search_engine.get('name')} Engine")

    driver.get(search_engine.get("start_url"))

    controller = SearchController(
        driver=driver, search_result_selectors=search_engine.get("selector")
    )

    items = controller.search(q=q)

    filtered_items = [
        item for item in items if item.get_attribute('href').find(f) != -1
    ]

    utils.logger.info(f'{main.__name__}: Filtered Search Results {len(items)}')

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

    return driver


driver = None
try:
    driver = main(q="site:merjob.com", f="merjob.com")
    input("ENTER")
except Exception as e:
    utils.logger.info(e)
    input("ENTER SOMETHING SOMETHING")

finally:
    driver.quit()
