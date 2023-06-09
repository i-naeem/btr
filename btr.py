from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from utils.find_elements import find_by_selectors
from selenium.webdriver.common.keys import Keys
from configs import ADVERTISEMENT_PAUSE_TIME
from utils.scrolls import scroll_to_element
from configs import ADVERTISEMENT_SELECTORS
from selenium.webdriver.common.by import By
from utils.scrolls import scroll_down
from utils.scrolls import scroll_up
from configs import MAX_TRAVERSES
from configs import MAX_TABS
from typing import List
import random
import time

SCROLL_DOWN: str = "DOWN"
SCROLL_UP: str = "UP"


class BTR:

    def __init__(self,
                 driver: WebDriver,
                 selectors: List[WebElement],
                 initial_anchors: List[WebElement],

                 max_tabs: int = MAX_TABS,
                 max_traverses: int = MAX_TRAVERSES
                 ):

        self.driver = driver
        self.max_tabs = max_tabs
        self.selectors = selectors
        self.max_traverses = max_traverses
        self.anchors: List[WebElement] = initial_anchors

        self.start_window = self.driver.current_window_handle
        self.next_window = None

        self.view_counter = 0
        self.PAUSE_TIMES = [0.5, 1.0, 1.5, 2]
        self.SCROLL_PAUSE_TIMES = [0.3, 0.5, 0.8]
        self.SCROLL_TO_ELEMENT_PAUSE_TIME = 1.9

        self.advertisements: List[WebElement] = []

    def run(self):
        max_t_counter = 1
        while max_t_counter <= MAX_TRAVERSES:
            tabs = self.open_tabs()
            self.view_tabs(tabs)

            self.next_window = random.choice(tabs)
            self.__close_windows()

            self.anchors = self.__find_anchors()

            max_t_counter = max_t_counter + 1

        self.advertisements = self.__find_advertisement()
        self.view_advertisement()
        self.__pause()
        self.__scroll()

    def view_tabs(self, tabs):
        for window in tabs:
            self.driver.switch_to.window(window)
            self.__pause()
            self.__scroll(direction=SCROLL_DOWN)
            self.view_counter = self.view_counter + 1

    def view_advertisement(self):
        for advertisement in self.advertisements:
            try:
                frame = advertisement.get('iframe')
                anchor = advertisement.get('anchor')
                scroll_to_element(
                    element=frame,
                    driver=self.driver,
                    pause=self.SCROLL_TO_ELEMENT_PAUSE_TIME
                )

                self.driver.switch_to.frame(frame)
                anchor.click()

                time.sleep(ADVERTISEMENT_PAUSE_TIME)
                return
            except Exception as e:
                print('FAILED TO CLICK ON AD')

            finally:
                self.driver.switch_to.default_content()

        self.driver.switch_to.default_content()

    def __close_windows(self):
        for window in self.driver.window_handles:
            if window == self.next_window:
                continue
            try:
                self.__pause()
                self.driver.switch_to.window(window)
                self.driver.close()
            except NoSuchWindowException as e:
                print('NoSuchWindow')

        self.driver.switch_to.window(self.next_window)

    def __scroll(self, direction=SCROLL_DOWN):
        scroll_pause = random.choice(self.SCROLL_PAUSE_TIMES)
        if direction == SCROLL_DOWN:
            scroll_down(driver=self.driver, pause=scroll_pause)
        else:
            scroll_up(driver=self.driver, pause=scroll_pause)

        self.__pause()

    def __pause(self) -> None:
        sleep_time = random.choice(self.PAUSE_TIMES)
        time.sleep(sleep_time)

    def open_tabs(self):
        tab_counter = 0
        for anchor in self.anchors:
            if tab_counter >= self.max_tabs:
                break
            scroll_to_element(
                element=anchor,
                driver=self.driver,
                pause=self.SCROLL_TO_ELEMENT_PAUSE_TIME
            )

            anchor.send_keys(Keys.CONTROL, Keys.ENTER)
            self.__pause()
            tab_counter = tab_counter + 1

        self.start_window = self.driver.current_window_handle
        tabs = [w for w in self.driver.window_handles if w != self.start_window]
        random.shuffle(tabs)
        return tabs

    def __find_anchors(self) -> List[WebElement]:
        return find_by_selectors(
            timeout=3,
            max_element=3,
            driver=self.driver,
            selectors=self.selectors,
        )

    def __find_advertisement(self) -> List[WebElement]:
        all_ads = []
        iframes = self.driver.find_elements(by=By.TAG_NAME, value="iframe")
        random.shuffle(iframes)
        for iframe in iframes:
            if len(all_ads) >= 3:
                break

            self.driver.switch_to.frame(iframe)
            elements = find_by_selectors(
                timeout=2,
                max_element=3,
                driver=self.driver,
                randomize_elements=False,
                selectors=ADVERTISEMENT_SELECTORS,

            )
            # Change the element to dictionary { iframe: active_iframe, anchor: anchor_element}
            all_ads.extend([dict(iframe=iframe, anchor=element) for element in elements])
            self.driver.switch_to.default_content()

        self.driver.switch_to.default_content()

        return all_ads
