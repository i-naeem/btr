from search_controller import SearchController
from selenium.webdriver.common.by import By
from utils import use_driver, use_logger
from bot import Bot

logger = use_logger()

driver = use_driver()
controller = SearchController(
    driver=driver,
    name="DuckDuckGo",
    searchbar_selector=(By.NAME, "q"),
    start_url="https://duckduckgo.com",
    results_selector=(By.CSS_SELECTOR, "a")
)

controller.search(q="site:merjob.com")

bot = Bot(
    selectors=[
        (By.CSS_SELECTOR, ".react-results--main h2 a"),
        (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
        (By.CSS_SELECTOR, ".entry-title a")
    ],
    driver=driver
)

bot.start()
