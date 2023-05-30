from utils import use_driver, scroll_to_element, scroll_down, scroll_up, use_logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from typing import List, Tuple
import random

logger = use_logging()


class Bot:
    def __init__(self,
                 driver: WebDriver,
                 selectors: List[Tuple(By.CSS_SELECTOR, str)],
                 ):
        logger.info('Creating the instance of Bot.')

        self.driver = driver
        self.selectors = selectors
        self.original_window = self.driver.current_window_handle

        self.wait = WebDriverWait(self.driver, 10)
        self.pages = self._find_pages()
        self.ads = self._find_ads()

    @property
    def all_tabs(self):
        return [w for w in self.driver.window_handles if w != self.original_window]

    def start(self) -> None:
        logger.info('Starting the bot and opening links')
        # Opens Random 5 Pages in New Tab
        for _ in range(5):

            element = random.choice(self.pages)
            scroll_to_element(self.driver, element)

            logger.info(f'Opening [{element.get_attribute("href")}] in new tab.')
            element.send_keys(Keys.CONTROL, Keys.ENTER)

        self.view()

    def view(self) -> None:
        # We view all the tabs one by one.
        logger.info('Viewing the opened tabs.')
        for window in self.all_tabs:
            logger.info(f'Switching to [{window}] tab.')
            self.driver.switch_to.window(window)
            scroll_down(self.driver)
            scroll_up(self.driver)
            scroll_down(self.driver)

        # Check if there more than one tab open then we switch randomly.
        if len(self.all_tabs) != 0:
            self.original_window = random.choice(self.all_tabs)
            logger.info(f'Changed the original window to [{self.original_window}]')
            for window in self.all_tabs:
                logger.info(f'Closing other opened tabs.')
                self.driver.switch_to.window(window)
                self.driver.close()

            logger.info(f'Switching to [{self.original_window}]')
            self.driver.switch_to.window(self.original_window)

        # else we stay on the original window scroll up and down.
        else:
            logger.info(f'No opened tabs were found so scrolling through orignal window.')
            scroll_down(self.driver)
            scroll_up(self.driver)
            scroll_down(self.driver)

    def _find_pages(self) -> List[WebElement]:
        elements = []
        logger.info(f'Finding pages on {self.original_window}')
        for selector in self.selectors:
            try:
                elements.extend(self.wait.until(EC.presence_of_all_elements_located(selector)))
            except TimeoutException:
                logger.error(f'There were no elements found for [ {selector = } ]')

        return elements

    def _find_ads(self):
        pass


if __name__ == '__main__':
    from selenium.webdriver.common.by import By

    driver = use_driver()
    driver.get("http://books.toscrape.com")

    selectors = [(By.CSS_SELECTOR, ".product_pod > h3 > a"),]

    bot = Bot(driver=driver, selectors=selectors)

    bot.start()
    input('Press enter to quit')
    driver.quit()
