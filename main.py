from selenium.webdriver.common.by import By
from utils import use_driver, use_proxies, use_logger
from joblib import delayed, Parallel
from bot import Bot
import env

logger = use_logger()


def main(proxy):
    protocol = proxy.get('protocol')
    server = proxy.get('server')
    port = proxy.get('port')
    uname = env.PROXY_USERNAME
    paswd = env.PROXY_PASSWORD

    driver = use_driver(
        username=uname,
        password=paswd,
        port=port,
        server=server,
        protocol=protocol,
    )

    q = "site:merjob.com"
    driver.get(f'https://duckduckgo.com/?va=v&t=ha&q={q}')

    bot = Bot(
        driver=driver,
        max_views=3,
        max_traverse=2,
        page_selectors=[
            (By.CSS_SELECTOR, '[data-testid="result-title-a"]'),
            (By.CSS_SELECTOR, '.entry-title a'),
            (By.CSS_SELECTOR, '.wp-block-latest-posts__post-title'),
            (By.CSS_SELECTOR, '.cat-item a'),
        ],
    )

    try:
        bot.start()
        logger.info('Finished one session.')
    except Exception as e:
        print(e)
        logger.error('FAILED!!!')

    finally:
        driver.quit()


proxies = use_proxies(max=21)
Parallel(n_jobs=3)(delayed(main)(proxy) for proxy in proxies)
