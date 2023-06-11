from utils.driver import use_driver
from bot import Bot
import settings
import logging
import random

# Setting Logger
logging.basicConfig(
    filename="./logs/btr.log",
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


def main():
    driver = use_driver()
    data = random.choice(settings.BLOG_DERA_JOBS_PK_DATA)

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
        bot.crawling()
    except Exception as e:
        logging.error('failed to finish session')
        logging.exception(e)

    finally:
        driver.quit()


main()
