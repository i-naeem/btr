from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from utils.find_elements import find_by_selectors
from typing import List
import random
import time


class BTR:
    def __init__(self,
                 driver: WebDriver,
                 selectors: List[WebElement],
                 initial_anchors: List[WebElement],
                 ):

        self.driver = driver
        self.selectors = selectors
        self.initial_anchors = initial_anchors

        self.SLEEP_TIMES = [0.5, 1.0, 1.5, 2]

    def __find_anchors(self) -> List[WebElement]:
        return find_by_selectors(
            timeout=3,
            max_element=3,
            driver=self.driver,
            selectors=self.selectors,
        )

    def __find_advertisement(self) -> List[WebElement]:
        return []

    def __pause(self) -> None:
        sleep_time = random.choice(self.SLEEP_TIMES)
        time.sleep(sleep_time)
