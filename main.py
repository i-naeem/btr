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

    q = "site:blog.derajobs.pk"
    driver.get(f'https://duckduckgo.com/?va=v&t=ha&q={q}')

    bot = Bot(
        driver=driver,
        max_views=2,
        max_traverse=3,
        page_selectors=[
            (By.CSS_SELECTOR, '[data-testid="result-title-a"]'),
            (By.CSS_SELECTOR, '.entry-title a'),
            (By.CSS_SELECTOR, '.entry-content a[href*="blog.derajobs.pk"]'),
            (By.ID, 'menu-item-17'),
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


proxies = use_proxies(max=5)

for proxy in proxies:
    main(proxy)
#Parallel(n_jobs=1)(delayed(main)(proxy) for proxy in proxies)
