from utils.proxies import use_proxies
from utils.driver import use_driver
from bot import Bot
import settings
import logging
import random
import dotenv
import sys

logger_n = sys.argv[1]

dotenv.load_dotenv()


# Setting Logger
logging.basicConfig(
    filename=f"./logs/btr_{logger_n}.log",
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s::%(levelname)s::%(filename)s[%(funcName)s]::%(name)s::%(message)s",
)


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
# Turning of selenium logger
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('seleniumwire').level = logging.ERROR


def main(proxy, click_on_ad=False):
    driver = use_driver(proxy)
    data = random.choice(settings.BLOG_DERA_JOBS_PK_DATA)

    source = data.get('source')
    logging.info(f'Selected Source: {source}')
    start_url = data.get('start_url')
    route_selectors = data.get('route_selectors')

    driver.get(start_url)
    bot = Bot(
        driver=driver,
        max_tabs=settings.MAX_TABS,
        route_selectors=route_selectors,
        max_traverse=settings.MAX_TRAVERSE,
    )

    try:
        bot.crawling(click_on_ad=click_on_ad)
    except Exception as e:
        logging.error('failed to finish session')
        logging.exception(e)

    finally:
        logging.info('Closing Browser....')
        driver.quit()


if __name__ == '__main__':
    for proxy in use_proxies(max=100):
        main(proxy, click_on_ad=True)
