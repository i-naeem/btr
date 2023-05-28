from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from dataclasses import astuple
from models import Selector
from typing import List
import utils
import random
import time


class Bot:
    def __init__(self,
                 available_pages: List[WebElement],
                 selectors: List[Selector],
                 driver: WebDriver,
                 max_views: int = 1,
                 max_tabs: int = 1,
                 ):
        self.available_pages = available_pages
        self.selectors = selectors
        self.max_views = max_views
        self.max_tabs = max_tabs
        self.driver = driver

        self.wait = WebDriverWait(self.driver, 10)

        self.next_starting_window = random.choice(self.driver.window_handles)
        self.original_window = self.driver.current_window_handle

    def start(self):
        utils.logger.info('Bot: Starting Bot')
        current_views = 0
        while current_views < self.max_views:
            current_tabs = 0

            utils.logger.info(f'Bot: Current Views: [{current_views}]')

            # Shuffle The Windows to Select Random Tab
            random.shuffle(self.driver.window_handles)
            # The next page that will be opened in new tab
            utils.logger.info(f'Bot: Selecting Next Page')
            next_page = random.choice(self.available_pages)
            # Scroll to the element (later it will be replaced by slow motion scroll)
            self.driver.execute_script('arguments[0].scrollIntoView()', next_page)

            # Open the new page in new tab and increment the tab count.

            utils.logger.info(f'Bot: Opening Next Page: {next_page.get_attribute("href")}')
            time.sleep(2)
            next_page.send_keys(Keys.CONTROL, Keys.ENTER)
            current_tabs += 1

            if current_tabs >= self.max_tabs:
                utils.logger.info(f'Bot: Selecting Next Starting Window')
                self.next_starting_window = random.choice(
                    [w for w in self.driver.window_handles
                        if w != self.original_window and w != self.next_starting_window]
                )
                utils.logger.info(f'Bot: Selected Next Starting Window {self.next_starting_window}')

                for tab in self.driver.window_handles:
                    if tab != self.original_window:
                        utils.logger.info(
                            f'Bot: Switching to {tab}')

                        self.driver.switch_to.window(tab)
                        time.sleep(2)
                        try:
                            if tab == self.next_starting_window:
                                self.view_page()
                                self._find_available_pages()
                            else:
                                self.view_page()
                                self.driver.close()
                        except Exception as e:
                            utils.logger.error(e)
                            if tab == self.next_starting_window:
                                self.next_starting_window = random.choice([
                                    w for w in self.driver.window_handles
                                    if w != self.original_window and w != self.next_starting_window
                                ])

                            else:
                                utils.logger.info(f'Bot: Closing {tab}')
                                self.driver.close()

                        current_views = current_views + 1
                        current_tabs = current_tabs - 1

            utils.logger.info(
                f'Bot: Switching back to Next Starting Window [{self.next_starting_window}]'
            )
            self.driver.switch_to.window(self.next_starting_window)
            time.sleep(2)
        utils.logger.info(
            f'Bot: Switching back to Original Window [{self.original_window}]'
        )
        self.driver.switch_to.window(self.original_window)
        time.sleep(2)

    def view_page(self):
        utils.logger.info(
            f'Bot: Viewing Page: [{self.driver.current_url}]'
        )
        self.wait.until(lambda d: d.execute_script(
            'return document.readyState === "interactive" || document.readyState === "complete"'))
        self.scroll_down()
        self.scroll_up()
        self.scroll_down()

        time.sleep(1)

    def scroll_down(self, speed: float = 2) -> None:
        max_scroll = self.driver.execute_script("return document.body.scrollHeight")

        actions = ActionChains(self.driver)
        scrolled_height = self.driver.execute_script(
            "return window.pageYOffset + window.innerHeight"
        )

        while scrolled_height < max_scroll:
            max_scroll = self.driver.execute_script("return document.body.scrollHeight")
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(random.uniform(1, speed))
            scrolled_height = self.driver.execute_script(
                "return window.pageYOffset + window.innerHeight"
            )

    def scroll_up(self, speed: float = 2) -> None:
        actions = ActionChains(self.driver)
        scrolled_height = self.driver.execute_script("return window.pageYOffset")

        while scrolled_height > 0:
            actions.send_keys(Keys.PAGE_UP).perform()
            time.sleep(random.uniform(1, speed))
            scrolled_height = self.driver.execute_script("return window.pageYOffset")

    def _find_available_pages(self):
        utils.logger.info(f'Bot: Finding Available Pages at {self.driver.current_url}')
        self.available_pages = []
        for selector in self.selectors:
            results = self.driver.find_elements(*astuple(selector))
            self.available_pages.extend(results)

        utils.logger.info(f'Bot: Found TOTAL {len(self.available_pages)}')
