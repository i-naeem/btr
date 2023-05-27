import time
import utils
import random
from typing import List, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class TrafficBot:
    def __init__(self,
                 selectors: List[Tuple[By, str]],
                 pages: List[WebElement],
                 driver: WebDriver,
                 views: int = 5
                 ):
        self.views = views
        self.pages = pages
        self.driver = driver
        self.selectors = selectors

    @property
    def is_pages_empty(self) -> bool:
        return len(self.pages) == 0

    def start(self) -> None:
        if self.is_pages_empty:
            print("The pages are empty can not process further")
            raise Exception("The pages are empty try again.")

        for _ in range(self.views):
            next_page = random.choice(self.pages)
            self.view_page(next_page)

            next_available_pages = []
            for selector in self.selectors:
                next_available_pages.extend(self.driver.find_elements(*selector))

            self.pages = next_available_pages

        return None

    def view_page(self, page: WebElement) -> None:
        utils.scroll_up_down(self.driver)
        self.driver.execute_script('window.scrollTo(0, screen.height/2)')
        time.sleep(random.uniform(2, 4))

        utils.virtual_click(self.driver, page)
        time.sleep(1)
