from utils import use_driver, scroll_to_element, scroll_down, scroll_up
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import random


class Bot:
    def __init__(self,
                 selectors,
                 driver: WebDriver):
        self.driver = driver
        self.selectors = selectors

        self.wait = WebDriverWait(self.driver, 10)
        self.pages = self._find_pages()
        self.ads = self._find_ads()

        self.original_window = self.driver.current_window_handle
        self.next_page = random.choice(self.pages) if len(self.pages) else None

    @property
    def all_tabs(self):
        return [w for w in self.driver.window_handles if w != self.original_window]

    def start(self):
        # Opens Random 5 Pages in New Tab
        for _ in range(5):
            element = random.choice(self.pages)
            scroll_to_element(self.driver, element)
            element.send_keys(Keys.CONTROL, Keys.ENTER)

        self.view()

    def view(self):
        # We view all the tabs one by one.
        for window in self.all_tabs:
            self.driver.switch_to.window(window)
            scroll_down(self.driver)
            scroll_up(self.driver)
            scroll_down(self.driver)

        # Check if there more than one tab open then we switch randomly.
        if len(self.all_tabs) != 0:
            self.original_window = random.choice(self.all_tabs)
            for window in self.all_tabs:
                self.driver.switch_to.window(window)
                self.driver.close()

            self.driver.switch_to.window(self.original_window)
        # else we stay on the original window scroll up and down.
        else:
            scroll_down(self.driver)
            scroll_up(self.driver)
            scroll_down(self.driver)

    def _find_pages(self):
        elements = []
        for selector in self.selectors:
            try:
                elements.extend(self.wait.until(EC.presence_of_all_elements_located(selector)))
            except TimeoutException:
                print(f"{selector} elements were not found")

        return elements

    def _find_ads(self):
        pass


if __name__ == '__main__':
    from selenium.webdriver.common.by import By

    driver = use_driver()
    driver.get("http://books.toscrape.com")

    selectors = [
        (By.CSS_SELECTOR, ".product_pod > h3 > a"),
    ]

    bot = Bot(
        driver=driver,
        selectors=selectors
    )

    bot.start()
    input('Press enter to quit')
    driver.quit()
