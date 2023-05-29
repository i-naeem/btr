from utils import use_driver, scroll_to_element, scroll_down, scroll_up
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import random


class Bot:
    def __init__(self,
                 driver,
                 selectors):
        self.driver = driver
        self.selectors = selectors

        self.wait = WebDriverWait(self.driver, 10)
        self.pages = self._find_pages()
        self.ads = self._find_ads()

        self.next_page = random.choice(self.pages) if len(self.pages) else None

    def goto(self, anchor):
        scroll_to_element(self.driver, anchor)
        anchor.click()

    def view(self):
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
        (By.CSS_SELECTOR, ".this-is-not-found"),
    ]

    bot = Bot(
        driver=driver,
        selectors=selectors
    )

    bot.goto(random.choice(bot.pages))
    input('Press enter to quit')
    driver.quit()
