from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from utils.find_elements import find_by_selectors
from utils.scrolls import scroll_down
from utils.scrolls import scroll_up
from typing import List
import random
import time

SCROLL_DOWN = "DOWN"
SCROLL_UP = "UP"


class BTR:

    def __init__(self,
                 driver: WebDriver,
                 selectors: List[WebElement],
                 initial_anchors: List[WebElement],
                 ):

        self.driver = driver
        self.selectors = selectors
        self.initial_anchors = initial_anchors

        self.PAUSE_TIMES = [0.5, 1.0, 1.5, 2]
        self.SCROLL_PAUSE_TIMES = [0.3, 0.5, 0.8]

    def __scroll(self, direction=SCROLL_DOWN):
        scroll_pause = random.choice(self.SCROLL_PAUSE_TIMES)
        if direction == SCROLL_DOWN:
            scroll_down(driver=self.driver, pause=scroll_pause)
            self.__pause()

        else:
            scroll_up(driver=self.driver, pause=scroll_pause)
            self.__pause()

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
        sleep_time = random.choice(self.PAUSE_TIMES)
        time.sleep(sleep_time)
