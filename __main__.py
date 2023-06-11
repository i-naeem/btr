from selenium.webdriver.common.by import By
from utils.driver import use_driver
from bot import Bot

driver = use_driver()
driver.get('https://books.toscrape.com')
bot = Bot(
    max_tabs=2,
    driver=driver,
    max_traverse=2,
    route_selectors=[(By.CSS_SELECTOR, '.nav.nav-list li a')]
)

bot.crawling()
