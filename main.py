from utils import use_driver, use_logger, use_proxies
from search_controller import SearchController
from selenium.webdriver.common.by import By
from bot import Bot

logger = use_logger()

selectors = [
    (By.CSS_SELECTOR, ".react-results--main h2 a"),
    (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
    (By.CSS_SELECTOR, ".entry-title a")
]


def use_duckduckgo(proxy={}, selectors=[], q=""):
    driver = use_driver(
        proxy_protocol=proxy.get('protocol'),
        proxy_server=proxy.get('server'),
        proxy_port=proxy.get('port')
    )

    controller = SearchController(
        driver=driver,
        name="DuckDuckGo",
        searchbar_selector=(By.NAME, "q"),
        start_url="https://duckduckgo.com",
        results_selector=(By.CSS_SELECTOR, "a")
    )

    controller.search(q=q)

    bot = Bot(
        selectors=selectors,
        driver=driver
    )

    try:
        bot.start(max_tabs_per_page=3)
        driver.quit()
    except Exception as e:
        driver.quit()
        raise e


proxies = use_proxies(max=3)

for i in range(5):
    logger.info('Selecting proxy')
    proxy = proxies[i % 3]
    try:
        for proxy in proxies:
            logger.info(f'Starting with proxy: {proxy}')
            use_duckduckgo(proxy, selectors, q="site:merjob.com")

    except Exception as e:
        logger.warning('failed to load proxies file make sure file exist and have correct path.')
        print(e)
