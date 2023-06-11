from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.by import By
from utils.driver import use_driver
from bot import Bot
import logging


logging.basicConfig(filename="btr.log", level=logging.INFO)

# Turning of selenium logger
LOGGER.setLevel(logging.WARNING)

start_url = 'https://books.toscrape.com'

logging.info('Starting driver...')
driver = use_driver()

logging.info(f'Opening the {start_url}...')
driver.get(start_url)

logging.info('Creating bot...')
bot = Bot(
    max_tabs=2,
    driver=driver,
    max_traverse=2,
    route_selectors=[(By.CSS_SELECTOR, '.nav.nav-list li a')]
)

logging.info('Start Crawling...')
bot.crawling()
