from selenium.webdriver.remote.webdriver import WebDriver
from utils.scrolls import scroll_down, scroll_up
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.driver import find_by_selectors
from typing import List, Tuple
import random

UP: str = "UP"
DOWN: str = "DOWN"
AD_SELECTORS: List[Tuple[str, str]] = [(By.CSS_SELECTOR, ".ad")]


class Bot:
    def __init__(self,
                 driver: WebDriver,
                 scroll_pause,
                 route_selectors,
                 ad_selectors=AD_SELECTORS,
                 ):
        self.driver = driver
        self.scroll_pause = scroll_pause
        self.ad_selectors = ad_selectors
        self.route_selectors = route_selectors

        self.available_ads = None
        self.available_routes = self.__find_routes()

        # The window where we clicked on the ad.
        self.ad_window = None
        # The window we will switch to.
        self.next_window = None
        # The window which was used to open tabs.
        self.traversing_window = self.driver.current_window_handle
        # The starting window of the bot.
        self.original_window = self.driver.current_window_handle

    def scroll(self, direction: str = DOWN):
        if direction == DOWN:
            scroll_down(self.driver, self.scroll_pause)
        else:
            scroll_up(self.driver, self.scroll_pause)

    def goto(self):
        random.shuffle(self.available_routes)

        for route in random.sample(self.available_routes, self.max_tabs):
            route.send_keys(Keys.CONTROL, Keys.ENTER)
        self.traversing_window = self.driver.current_window_handle

    def goto_ad(self):
        ad = random.choice(self.available_ads)
        frame = getattr(ad, 'iframe', None)
        anchor = getattr(ad, 'anchor', None)

        self.driver.switch_to.frame(frame)
        anchor.click()

        self.ad_window = self.driver.current_window_handle

    def __find_ads(self):
        all_ads = []
        for iframe in self.driver.find_elements(by=By.TAG_NAME, value="iframe"):
            if len(all_ads) >= 4:
                break

            self.driver.switch_to.frame(iframe)
            elements = find_by_selectors(self.driver, self.ad_route_selectors)
            # Change the element to dictionary { iframe: active_iframe, anchor: anchor_element}
            all_ads.extend([dict(iframe=iframe, anchor=element) for element in elements])
            self.driver.switch_to.default_content()

    def __find_routes(self):
        # TODO: Change the max to maximum tab opens.
        return find_by_selectors(self.driver, self.route_selectors)
