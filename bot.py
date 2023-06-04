from utils import find_by_selectors
from selenium.webdriver.common.by import By


class Bot:
    def __init__(self,
                 driver,
                 page_selectors,
                 advertisement_selectors,

                 ):

        self.driver = driver
        self.page_selectors = page_selectors
        self.advertisement_selectors = advertisement_selectors

        self.pages = find_by_selectors(self.driver, page_selectors)


def main():
    from utils import use_driver

    driver = use_driver()
    driver.get('https://jobsbox.pk')
    bot = Bot(
        driver=driver,
        page_selectors=[(By.CSS_SELECTOR, '.entry-title a')],
        advertisement_selectors=[(By.CSS_SELECTOR, '.entry-title a')]
    )

    print(bot.pages)


if __name__ == '__main__':
    main()
