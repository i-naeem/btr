from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchWindowException
from utils.scrolls import scroll_down, scroll_up
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.driver import find_by_selectors
from typing import List, Tuple
import logging
import random
import time


bot_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(filename="./logs/bot.log", mode="w", encoding="utf-8")
log_format = logging.Formatter('%(asctime)s::%(levelname)s::%(message)s')
bot_logger.addHandler(file_handler)

UP: str = "UP"
DOWN: str = "DOWN"
AD_SELECTORS: List[Tuple[str, str]] = [(By.CSS_SELECTOR, ".ad")]


class Bot:
    def __init__(self,
                 driver: WebDriver,
                 route_selectors: List[Tuple[str, str]],

                 max_tabs: int = 2,
                 max_traverse: int = 3,
                 scroll_pause: float = random.uniform(1, 2),
                 ad_selectors: List[Tuple[str, str]] = AD_SELECTORS,
                 ):
        self.route_selectors = route_selectors
        self.scroll_pause = scroll_pause
        self.ad_selectors = ad_selectors
        self.max_traverse = max_traverse
        self.max_tabs = max_tabs
        self.driver = driver

        self.view_count = 0
        self.available_ads = None
        self.available_routes = None

        # The window we will switch to.
        self.next_window = None
        # The window which was used to open tabs.
        self.traversing_window = self.driver.current_window_handle
        # The starting window of the bot.
        self.original_window = self.driver.current_window_handle

    @property
    def new_tabs(self):
        windows = [w for w in self.driver.window_handles
                   if w != self.traversing_window and w != self.original_window]
        random.shuffle(windows)
        return windows

    def crawling(self):
        logging.info('Crawling...')

        start_time = time.time()
        for _ in range(self.max_traverse):
            self.start()

        session = time.time() - start_time
        logging.info(f'We viewed {self.view_count} pages in {session:.3f} seconds.')

    def start(self):
        self.available_routes = self.__find_routes()
        self.scroll(direction=DOWN)
        self.scroll(direction=UP)
        self.goto()

        logging.info('Switching an viewing windows...')
        for window in self.new_tabs:
            self.view_count = self.view_count + 1

            start_time = time.time()
            self.driver.switch_to.window(window)

            logging.info(f'Switched to {self.driver.title}')
            self.scroll(direction=DOWN)
            self.scroll(direction=UP)

            session = time.time() - start_time
            bot_logger.info(f'{self.driver.current_url} [{session:.3f}]')

        logging.info('Selecting next window')
        self.next_window = random.choice(self.new_tabs)
        self.driver.switch_to.window(self.next_window)

        self.close_windows()

    def close_windows(self):
        logging.info('Closing extra windows...')
        for window in self.driver.window_handles:
            if window != self.next_window:
                try:
                    self.driver.switch_to.window(window)
                    logging.info(f'Closing {self.driver.title} window...')
                    self.driver.close()
                except NoSuchWindowException as e:
                    logging.warning(f'failed to close window')
                    logging.exception(e)

        self.driver.switch_to.window(self.next_window)
        self.original_window = self.next_window
        self.next_window = None

    def scroll(self, direction: str = DOWN):
        if direction == DOWN:
            logging.info('Scrolling down...')
            scroll_down(self.driver, self.scroll_pause)
        else:
            logging.info('Scrolling up...')
            scroll_up(self.driver, self.scroll_pause)

    def goto(self):
        random.shuffle(self.available_routes)
        for route in random.sample(self.available_routes, self.max_tabs):
            logging.info(f'Starting new tab of {route.text}...')
            route.send_keys(Keys.CONTROL, Keys.ENTER)

        self.traversing_window = self.driver.current_window_handle

    def goto_ad(self):
        ad = random.choice(self.available_ads)
        frame = getattr(ad, 'iframe', None)
        anchor = getattr(ad, 'anchor', None)

        self.driver.switch_to.frame(frame)
        anchor.click()

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
