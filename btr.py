from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from utils.find_elements import find_by_selectors
from selenium.webdriver.common.keys import Keys
from utils.scrolls import scroll_to_element
from utils.scrolls import scroll_down
from utils.scrolls import scroll_up
from configs import MAX_TABS
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

                 max_tabs: int = MAX_TABS
                 ):

        self.driver = driver
        self.max_tabs = max_tabs
        self.selectors = selectors
        self.initial_anchors = initial_anchors

        self.start_window = self.driver.current_window_handle
        self.next_window = None

        self.anchors: List[WebElement] = []
        self.PAUSE_TIMES = [0.5, 1.0, 1.5, 2]
        self.SCROLL_PAUSE_TIMES = [0.3, 0.5, 0.8]

    def open_tabs(self):
        tab_counter = 0
        scroll_pause = random.choice(self.SCROLL_PAUSE_TIMES)
        for anchor in self.anchors:
            if tab_counter >= self.max_tabs:
                break
            scroll_to_element(driver=self.driver, element=anchor, pause=scroll_pause)
            anchor.send_keys(Keys.CONTROL, Keys.ENTER)
            self.__pause()

        self.start_window = self.driver.current_window_handle

    def __close_windows(self):
        for window in self.driver.window_handles:
            if window == self.next_window:
                continue
            try:
                self.driver.switch_to.window(window)
                self.__pause()
                self.driver.close()
            except NoSuchWindowException as e:
                print('NoSuchWindow')
                pass

        self.driver.switch_to.window(self.next_window)
        self.start_window = self.next_window
        self.next_window = None

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
