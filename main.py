
import env
import random
import configs
from SearchBot import SearchBot
from TrafficBot import TrafficBot
from proxies import PROXIES, Proxy
from joblib import Parallel, delayed
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service


def start_bot(query: str, filter_text: str = None, proxy: Proxy = None, ):

    service = Service(executable_path=env.CHROME_EXECUTABLE_PATH)
    chrome_options = ChromeOptions()

    if proxy:
        chrome_options.add_argument(
            f'--proxy-server={proxy.protocol}://{proxy.server}:{proxy.port}'
        )

    driver = Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(5)

    def f(el):
        return el.get_attribute('href').lower().find(filter_text) != -1

    search_bot = SearchBot(driver=driver, **configs.GOOGLE_CONFIGS)

    search_results = search_bot.search(
        query=query,
        fltr=f if filter_text else None
    )

    selectors = [
        (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
        (By.CSS_SELECTOR, ".entry-title > a")
    ]

    bot = TrafficBot(
        selectors=selectors,
        pages=search_results,
        driver=driver,
        views=3
    )

    try:
        bot.start()
    except:
        print("FAILED!!!")


Parallel(n_jobs=1)(delayed(start_bot)(proxy=proxy,
                                      query="site:merjob.com",
                                      filter_text="merjob.com")
                   for proxy in random.sample(PROXIES, 2)
                   )
