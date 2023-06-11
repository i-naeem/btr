from utils import find_by_selectors, scroll_down, scroll_up, scroll_to_element
from constants import DEFAULT_AD_SELECTORS, LOGGER
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from typing import List, Tuple
import logging
import random
import time


from selenium.webdriver.remote.webdriver import WebDriver


class Bot:
    def __init__(self,
                 driver: WebDriver,
                 page_selectors: List[Tuple[str, str]],
                 max_views: int = 3,
                 max_traverse: int = 1,
                 advertisement_selectors: List[Tuple[str, str]] = DEFAULT_AD_SELECTORS,
                 ):

        self.driver = driver
        self.max_views = max_views
        self.max_traverse = max_traverse
        self.page_selectors = page_selectors
        self.advertisement_selectors = advertisement_selectors

        self.views_count = 0
        self.logger = logging.getLogger(LOGGER)

    @property
    def rpause(self):  # random pause value
        return random.uniform(1, 2)

    def start(self):
        for _ in range(self.max_traverse):
            available_pages = self._find_available_pages()
            random.shuffle(available_pages)

            tab_count = 1
            for anchor in available_pages:
                if (tab_count > self.max_views):
                    break
                try:
                    self._click(anchor)
                    tab_count = tab_count + 1
                except Exception as e:
                    print("FAILED TO OPEN TAB!!")

            original_window = self.driver.current_window_handle
            tabs = [w for w in self.driver.window_handles if w != original_window]
            time.sleep(self.rpause)
            random.shuffle(tabs)
            time.sleep(self.rpause)

            for tab in tabs:
                self.driver.switch_to.window(tab)
                time.sleep(self.rpause)
                self.view_page()

            ad_tab = random.choice(tabs)

            for tab in self.driver.window_handles:
                if tab == ad_tab:
                    continue

                self.driver.switch_to.window(tab)
                time.sleep(self.rpause)
                self.driver.close()

            self.driver.switch_to.window(ad_tab)
        self.view_ad()

    def view_ad(self):
        ads = self._find_available_ads()
        for ad in ads:
            try:
                frame = ad.get('frame')
                element = ad.get('element')
                scroll_to_element(self.driver, frame)
                time.sleep(self.rpause)
                self.driver.switch_to.frame(frame)
                element.click()
                time.sleep(75)
                self.driver.back()
                time.sleep(self.rpause)
                break
            except Exception as e:
                self.logger.error('There was an error viewing the ad.')

            self.driver.switch_to.default_content()

        self.driver.switch_to.default_content()

    def view_page(self):
        scroll_down(self.driver, self.rpause)
        scroll_up(self.driver, self.rpause)
        time.sleep(self.rpause)

        self.views_count = self.views_count + 1
        self.logger.info(f'Viewed {self.views_count} pages...')

    def _click(self, anchor):
        scroll_to_element(self.driver, anchor)
        time.sleep(self.rpause)
        anchor.send_keys(Keys.CONTROL, Keys.ENTER)
        time.sleep(self.rpause)

    def _find_available_pages(self):
        return find_by_selectors(self.driver, self.page_selectors)

    def _find_available_ads(self):
        all_ads = []
        frames = self.driver.find_elements(by=By.TAG_NAME, value='iframe')
        random.shuffle(frames)
        for frame in frames:
            self.driver.switch_to.frame(frame)
            if len(all_ads) > 5:
                break

            elements = find_by_selectors(self.driver, self.advertisement_selectors)
            for element in elements:
                all_ads.append(dict(frame=frame, element=element))

            self.driver.switch_to.default_content()

        self.driver.switch_to.default_content()
        return all_ads


def main():
    from utils import use_driver, use_proxies
    import env

    proxies = use_proxies(max=1)
    proxy = proxies[0]

    driver = use_driver(
        port=proxy.get('port'),
        server=proxy.get('server'),
        protocol=proxy.get('protocol'),
        username=env.PROXY_USERNAME,
        password=env.PROXY_PASSWORD,

    )

    driver.get('https://derajobs.pk/')
    bot = Bot(
        driver=driver,
        max_views=1,
        max_traverse=1,
        page_selectors=[
            (By.CSS_SELECTOR, '.entry-title a'),
            (By.CSS_SELECTOR, '.cat-item'),
        ],
    )

    bot.start()


if __name__ == '__main__':
    main()

    input("Press enter to quit.")
