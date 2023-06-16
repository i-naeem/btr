from utils.scrolls import scroll_down, scroll_up, scroll_to_element
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.driver import find_by_selectors
from typing import List, Tuple
import logging
import random
import time
import sys

logger_n = sys.argv[1]

# Setting up logger
bot_logger = logging.getLogger(f"{__name__}_{logger_n}")
file_handler = logging.FileHandler(
    filename=f"./logs/bot_{logger_n}.log", mode="a", encoding="utf-8"
)
log_format = logging.Formatter('%(asctime)s::%(levelname)s::%(message)s')
bot_logger.addHandler(file_handler)

# Useful Constants
UP: str = "UP"
DOWN: str = "DOWN"
SELECTOR_LIST_TYPE = List[Tuple[str, str]]
AD_SELECTORS: SELECTOR_LIST_TYPE = [
    (By.CSS_SELECTOR, 'a[href*="adclick"]'),
    (By.CSS_SELECTOR, 'a[href*="doubleclick"]'),
    (By.CSS_SELECTOR, 'a[href*="googleadservice"]'),
]


class Bot:
    def __init__(self,
                 driver: WebDriver,
                 route_selectors: SELECTOR_LIST_TYPE,

                 max_tabs: int = 2,
                 max_traverse: int = 3,
                 ad_selectors: SELECTOR_LIST_TYPE = AD_SELECTORS,
                 ):
        self.route_selectors = route_selectors
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

        self.RANDOM_SLEEP_TIMES = [0.5, 1.0, 1.5, 2., 2.5]

    @property
    def new_tabs(self):
        windows = [w for w in self.driver.window_handles
                   if w != self.traversing_window and w != self.original_window]
        random.shuffle(windows)
        return windows

    def crawling(self, click_on_ad: False):
        logging.info('Crawling...')

        start_time = time.time()
        for _ in range(self.max_traverse):
            self.start()

        session = time.time() - start_time
        logging.info(f'We viewed {self.view_count} pages in {session:.3f} seconds.')

        if click_on_ad:
            logging.info('Trying to click on ad...')
            self.available_ads = self.__find_ads()
            random.shuffle(self.available_ads)
            self.goto_ad()
            logging.info('Ad Viewing Completed')

    def start(self):
        self.available_routes = self.__find_routes()
        self.scroll(direction=DOWN)
        self.goto()

        logging.info('Switching and viewing windows...')
        for window in self.new_tabs:
            self.view_count = self.view_count + 1

            start_time = time.time()
            self.driver.switch_to.window(window)
            self.__pause()

            logging.info(f'Switched to {self.driver.title}')
            self.scroll(direction=DOWN)

            session = time.time() - start_time
            bot_logger.info(f'{self.driver.current_url} [{session:.3f}]')

        logging.info('Selecting next window')

        try:
            self.next_window = random.choice(self.new_tabs)
        except Exception as e:
            logging.info('failed to switch to next window staying on the same window')
            self.next_window = self.driver.current_window_handle

        self.driver.switch_to.window(self.next_window)
        self.__pause()

        self.close_windows()

    def close_windows(self):
        logging.info('Closing extra windows...')
        for window in self.driver.window_handles:
            if window != self.next_window:
                try:
                    self.driver.switch_to.window(window)
                    self.__pause()
                    logging.info(f'Closing {self.driver.title} window...')
                    self.driver.close()
                    self.__pause()
                except NoSuchWindowException as e:
                    logging.warning(f'failed to close window')
                    logging.exception(e)

        self.driver.switch_to.window(self.next_window)
        self.original_window = self.next_window
        self.next_window = None

    def scroll(self, direction: str = DOWN):
        pause = random.choice([0.3, 0.5, 0.8, 1])
        if direction == DOWN:
            logging.info('Scrolling down...')
            scroll_down(self.driver, pause)
            self.__pause()
        else:
            logging.info('Scrolling up...')
            scroll_up(self.driver, random.choice([0.3, 0.4, 0.5]))
            self.__pause()

    def goto(self):
        random.shuffle(self.available_routes)
        tc = 0  # Tab Counter
        for route in self.available_routes:
            if tc >= self.max_tabs:
                break
            logging.info(f'Starting new tab of {route.text}...')
            scroll_to_element(self.driver, route)
            route.send_keys(Keys.CONTROL, Keys.ENTER)
            self.__pause()
            tc = tc + 1

        self.traversing_window = self.driver.current_window_handle

    def goto_ad(self):
        random.shuffle(self.available_ads)
        for ad in self.available_ads:

            try:
                frame = ad.get('iframe')
                anchor = ad.get('anchor')

                logging.info('Scrolling to IFRAME..')
                scroll_to_element(self.driver, frame)
                logging.info('Switching IFRAME..')
                self.driver.switch_to.frame(frame)
                logging.info('Clicking on ad.')
                anchor.click()
                logging.info('Waiting for 40 seconds.')
                time.sleep(40)
                return
            except Exception as e:
                logging.warning('Failed to click on ad trying again')
                logging.exception(e)

            finally:
                self.driver.switch_to.default_content()

        self.driver.switch_to.default_content()

    def __find_ads(self):
        all_ads = []
        iframes = self.driver.find_elements(by=By.TAG_NAME, value="iframe")
        random.shuffle(iframes)
        for iframe in iframes:
            if len(all_ads) >= 4:
                break

            self.driver.switch_to.frame(iframe)
            elements = find_by_selectors(self.driver, self.ad_selectors)
            # Change the element to dictionary { iframe: active_iframe, anchor: anchor_element}
            all_ads.extend([dict(iframe=iframe, anchor=element) for element in elements])
            self.driver.switch_to.default_content()

        self.driver.switch_to.default_content()

        return all_ads

    def __find_routes(self):
        # TODO: Change the max to maximum tab opens.
        return find_by_selectors(
            timeout=5,
            driver=self.driver,
            max_element=self.max_tabs,
            selectors=self.route_selectors,
        )

    def __pause(self):
        time.sleep(random.choice(self.RANDOM_SLEEP_TIMES))
