from utils import use_driver, scroll_to_element, scroll_down, scroll_up
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from logging import getLogger
from typing import List
import constants
import random
import time


class Bot:
    def __init__(self,
                 selectors,
                 driver: WebDriver):
        self.logger = getLogger(constants.LOGGER)
        self.logger.info('Creating the instance of Bot.')

        self.driver = driver
        self.selectors = selectors
        self.original_window = self.driver.current_window_handle

        self.wait = WebDriverWait(self.driver, 10)
        # self.pages = self._find_pages()
        self.ads = self._find_ads()

    @property
    def all_tabs(self):
        return [w for w in self.driver.window_handles if w != self.original_window]

    def start(self) -> None:
        self.logger.info('Starting the bot and opening links')
        # Opens Random 5 Pages in New Tab
        for _ in range(5):

            element = random.choice(self.pages)
            scroll_to_element(self.driver, element)
            time.sleep(2)
            self.logger.info(f'Opening [{element.get_attribute("href")}] in new tab.')
            element.send_keys(Keys.CONTROL, Keys.ENTER)
            time.sleep(2)

        self.view()

    def view(self) -> None:
        # We view all the tabs one by one.
        self.logger.info('Viewing the opened tabs.')
        for window in self.all_tabs:
            self.logger.info(f'Switching to [{window}] tab.')
            self.driver.switch_to.window(window)
            time.sleep(2)
            scroll_down(self.driver, pause=random.uniform(1, 2))
            scroll_up(self.driver, pause=random.uniform(1, 2))
            scroll_down(self.driver, pause=random.uniform(1, 2))

        # Check if there more than one tab open then we switch randomly.
        if len(self.all_tabs) != 0:
            self.original_window = random.choice(self.all_tabs)
            self.logger.info(f'Changed the original window to [{self.original_window}]')
            for window in self.all_tabs:
                self.logger.info(f'Closing other opened tabs.')
                self.driver.switch_to.window(window)
                time.sleep(2)
                self.driver.close()

            self.logger.info(f'Switching to [{self.original_window}]')
            self.driver.switch_to.window(self.original_window)
            time.sleep(2)
        # else we stay on the original window scroll up and down.
        else:
            self.logger.info(f'No opened tabs were found so scrolling through orignal window.')
            scroll_down(self.driver, pause=random.uniform(1, 2))
            scroll_up(self.driver, pause=random.uniform(1, 2))
            scroll_down(self.driver, pause=random.uniform(1, 2))

    def view_ad(self) -> None:
        # TODO: Make sure the tab we select to view ad is not our next window tab.
        source = self.driver.current_url
        for retry_count in range(5):

            ad_data = random.choice(self.ads)

            try:
                ad: WebElement = ad_data.get('element')
                frame = ad_data.get('frame')
                self.driver.switch_to.frame(frame)
                self.logger.info('Viewing ad...')

                ad.click()
                if source == self.driver.current_url:
                    self.logger.info(f'Trying ad for {retry_count} time(s).')
                    self.ads = [a for a in self.ads if ad != a]
                    continue
                pause = random.uniform(2, 3)
                scroll_down(self.driver, pause=pause)
                scroll_up(self.driver, pause=pause)
                scroll_down(self.driver, pause=pause)
                self.driver.back()

            except Exception as e:
                self.logger.error('Failed to view ad.')
                print(e)

    def _find_pages(self) -> List[WebElement]:
        elements = []
        self.logger.info(f'Findin pages on {self.original_window}')
        for selector in self.selectors:
            try:
                elements.extend(self.wait.until(EC.presence_of_all_elements_located(selector)))
            except TimeoutException:
                self.logger.error(f'There were no elements found for [ {selector = } ]')

        return elements

    def _find_ads(self) -> List[WebElement]:
        ads = []
        frames = self.wait.until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )

        self.logger.info('Switching through frames')
        for frame in frames:
            if len(ads) > 8:
                break
            self.driver.switch_to.frame(frame)
            for domain in constants.COMMON_ADS_DOMAINS:
                self.logger.info(f'Searching ads for {domain = }.')
                try:
                    ads_elements = self.wait.until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, f"a[href*='{domain}']")
                        )
                    )

                    for el in ads_elements:
                        ads.append(dict(frame=frame, element=el))
                except TimeoutException as e:
                    self.logger.warning(f'Failed to find any ads with {domain} domain.')

            self.driver.switch_to.parent_frame()

        self.driver.switch_to.default_content()

        return ads


if __name__ == '__main__':
    from selenium.webdriver.common.by import By
    from utils import use_logger

    use_logger()
    driver = use_driver()
    driver.get("https://derajobs.pk")

    selectors = [
        (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
        (By.CSS_SELECTOR, ".entry-title a"),
    ]

    bot = Bot(driver=driver, selectors=selectors)

    bot.view_ad()
    input('Press enter to quit')
    driver.quit()
