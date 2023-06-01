from utils import use_driver, scroll_to_element, scroll_down, scroll_up
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from logging import getLogger
from typing import List
import constants
import random
import time


class Bot:
    def __init__(self,
                 selectors,
                 driver: WebDriver):
        self.logger = getLogger(constants.LOGGER)
        self.logger.info('Creating the instance of Bot.')

        self.driver = driver
        self.selectors = selectors
        self.original_window = self.driver.current_window_handle

        self.wait = WebDriverWait(self.driver, 10)
        self.pages = self._find_pages()
        self.ads = self._find_ads()

    @property
    def all_tabs(self):
        return [w for w in self.driver.window_handles if w != self.original_window]

    def start(self, max_tabs_per_page: int = 3) -> None:
        self.logger.info('Starting the bot and opening links')
        # Opens Random 5 Pages in New Tab
        for _ in range(max_tabs_per_page % 5):  # no more than 5
            for _ in range(max_tabs_per_page):

                element = random.choice(self.pages)
                scroll_to_element(self.driver, element)
                time.sleep(random.uniform(2, 3))
                self.logger.info(f'Opening [{element.get_attribute("href")}] in new tab.')
                element.send_keys(Keys.CONTROL, Keys.ENTER)
                time.sleep(random.uniform(2, 3))

            self.view()
            self.pages = self._find_pages()

    def view(self) -> None:
        # We view all the tabs one by one.
        self.logger.info('Viewing the opened tabs.')
        for window in self.all_tabs:
            self.logger.info(f'Switching to [{window}] tab.')
            self.driver.switch_to.window(window)
            time.sleep(random.uniform(3, 4))
            scroll_down(self.driver, pause=random.uniform(2, 3))
            scroll_up(self.driver, pause=random.uniform(2, 3))
            scroll_down(self.driver, pause=random.uniform(2, 3))

        # Check if there more than one tab open then we switch randomly.
        if len(self.all_tabs) != 0:
            self.original_window = random.choice(self.all_tabs)
            self.logger.info(f'Changed the original window to [{self.original_window}]')
            for window in self.all_tabs:
                self.logger.info(f'Closing other opened tabs.')
                self.driver.switch_to.window(window)
                time.sleep(2)
                self.driver.close()

            self.logger.info(f'Switching to [{self.original_window}]')
            self.driver.switch_to.window(self.original_window)
            time.sleep(2)
        # else we stay on the original window scroll up and down.
        else:
            self.logger.info(f'No opened tabs were found so scrolling through orignal window.')
            scroll_down(self.driver, pause=random.uniform(1, 2))
            scroll_up(self.driver, pause=random.uniform(1, 2))
            scroll_down(self.driver, pause=random.uniform(1, 2))

    def _find_pages(self) -> List[WebElement]:
        elements = []
        self.logger.info(f'Findin pages on {self.original_window}')
        for selector in self.selectors:
            try:
                elements.extend(self.wait.until(EC.presence_of_all_elements_located(selector)))
            except TimeoutException:
                self.logger.error(f'There were no elements found for [ {selector = } ]')

        return elements

    def _find_ads(self):
        pass


if __name__ == '__main__':
    from selenium.webdriver.common.by import By
    from utils import use_logger

    use_logger()
    driver = use_driver()
    driver.get("https://merjob.com")

    selectors = [
        (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
        (By.CSS_SELECTOR, ".entry-title a"),
    ]

    bot = Bot(driver=driver, selectors=selectors)

    bot.start()
    input('Press enter to quit')
    driver.quit()
