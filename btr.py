from selenium.webdriver.remote.webelement import WebElement
from typing import List
import random
import time


class BTR:
    def __init__(self,
                 driver,
                 selectors,
                 initial_anchors,
                 ):

        self.driver = driver
        self.selectors = selectors
        self.initial_anchors = initial_anchors

        self.SLEEP_TIMES = [0.5, 1.0, 1.5, 2]

    def __find_anchors(self) -> List[WebElement]:

        return []

    def __find_advertisement(self) -> List[WebElement]:
        return []

    def __pause(self) -> None:
        sleep_time = random.choice(self.SLEEP_TIMES)
        time.sleep(sleep_time)
