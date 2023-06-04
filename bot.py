from utils import find_by_selectors, scroll_down, scroll_up, scroll_to_element
from selenium.webdriver.common.by import By
import random
import time


from selenium.webdriver.remote.webdriver import WebDriver


class Bot:
    def __init__(self,
                 driver: WebDriver,
                 page_selectors,
                 advertisement_selectors,
                 ):

        self.driver = driver
        self.page_selectors = page_selectors
        self.advertisement_selectors = advertisement_selectors

    @property
    def available_pages(self):
        return find_by_selectors(self.driver, self.page_selectors)

    @property
    def rpause(self):  # random pause value
        return random.uniform(2, 4)

    def start(self):
        pass

    def view_page(self, anchor):
        self._click(anchor)
        scroll_down(self.driver, self.rpause)
        scroll_up(self.driver, self.rpause)
        scroll_down(self.driver, self.rpause)

    def _click(self, anchor):
        # scroll_to_element(self.driver, anchor)
        anchor.click()
        time.sleep(self.rpause)

    def _find_available_ads(self):
        all_ads = []

        for frame in self.driver.find_elements(by=By.TAG_NAME, value='iframe'):
            self.driver.switch_to.frame(frame)
            if len(all_ads) > 10:
                break

            elements = find_by_selectors(self.driver, self.advertisement_selectors)
            for element in elements:
                all_ads.append(dict(frame=frame, element=element))

            self.driver.switch_to.default_content()
        return all_ads


def main():
    from utils import use_driver

    driver = use_driver()
    driver.get('https://www.yourfabulouslives.com/')
    bot = Bot(
        driver=driver,
        page_selectors=[(By.CSS_SELECTOR, '.entry-title a')],
        advertisement_selectors=[
            (By.CSS_SELECTOR, 'a[href*="adclick"]'),
            (By.CSS_SELECTOR, 'a[href*="doubleclick"]'),
            (By.CSS_SELECTOR, 'a[href*="googleadservice"]'),
        ]
    )

    bot.start()
    input("ENTER: ")


if __name__ == '__main__':
    main()
