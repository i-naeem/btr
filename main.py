
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome
from joblib import Parallel, delayed
from TrafficBot import TrafficBot
from SearchBot import SearchBot
from proxies import PROXIES
import configs
import random
import utils
import env


def start_bot(proxy, query, filter_text):
    print(proxy)
    service = Service(executable_path=env.CHROME_EXECUTABLE_PATH)
    chrome_options = utils.get_chrome_options(
        proxy=proxy,
        ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    )

    driver = Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(5)

    for retry in range(3):
        try:
            def f(el): return el.get_attribute('href').lower().find(filter_text) != -1

            search_bot = SearchBot(driver=driver, **configs.DUCKDUCKGO)

            search_results = search_bot.search(
                query=query,
                fltr=f if filter_text else None
            )

            selectors = [
                (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
                (By.CSS_SELECTOR, ".entry-title > a")
            ]

            bot = TrafficBot(
                driver=driver,
                selectors=selectors,
                pages=search_results,
                views=random.randint(2, 4)
            )

            bot.start()
            print("Finished...")
            break

        except Exception as e:
            print(f"ERROR: {e}")

        finally:
            print(f"[{retry}] Retring....")
    else:
        driver.quit()


Parallel(n_jobs=2)(
    delayed(start_bot)(proxy, "site:merjob.com", "merjob.com") for proxy in PROXIES
)
