from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
import random
import time


class BTR:
    def __init__(self,
                 driver,
                 max_tabs=5,
                 anchor_selectors=(By.CSS_SELECTOR, 'a'),
                 advertisement_selectors=(By.CSS_SELECTOR, '[href*="google"]'),
                 ):

        self.driver = driver
        self.max_tabs = max_tabs
        self.anchor_selectors = anchor_selectors
        self.advertisement_selectors = advertisement_selectors

        self.original_tab = self.driver.current_window_handle
        self.anchors = self._find_anchors()

    @property
    def new_tabs(self):
        new_tabs = [w for w in self.driver.window_handles if w != self.original_tab]
        random.shuffle(new_tabs)
        return new_tabs

    def start(self, max_view=5, max_ad_click=3):
        for _ in range(max_view):
            self.view()
            # Update anchors for current page

            self.view_ad()

            self.anchors = self._find_anchors()
            for tab in self.new_tabs:
                self.driver.switch_to.window(tab)
                self.driver.close()

            self.driver.switch_to.window(self.original_tab)

    def view(self):
        random.shuffle(self.anchors)

        # Open 5 tabs
        for anchor in random.sample(self.anchors, self.max_tabs % len(self.anchor)):
            anchor.send_keys(Keys.CONTROL, Keys.ENTER)

        # View all tabs
        for tab in self.new_tabs:
            self.driver.switch_to.window(tab)
            self.scroll_down()
            self.scroll_up()
            self.scroll_up()

        self.driver.switch_to.window(self.original_tab)

        # Select next tab
        self.original_tab = random.choice(self.new_tabs)

        # Close all tabs

    def view_ad(self):
        for tab in self.new_tabs:
            advertisements = self._find_advertisements()
            if len(advertisements) != 0:
                for retry in 5:
                    try:
                        source_url = self.driver.current_url
                        advertisement = random.choice(advertisements)
                        ad_anchor = advertisement.get('anchor')
                        ad_frame = advertisement.get('frame')
                        self.driver.switch_to.frame(ad_frame)
                        ad_anchor.click()
                        if self.driver.current_url == source_url:
                            raise Exception("click did not work.")
                        self.pause(4)
                        self.driver.back()
                        self.driver.switch_to.default_content()
                        print('AD VIEWED')
                        break
                    except Exception as e:
                        print(e)

    def pause(self, mm):
        time.sleep(mm)

    def scroll_down(self):
        body = self.driver.find_element(by=By.TAG_NAME, value='body')
        body.send_keys(Keys.END)
        self.pause(2)

    def scroll_up(self):
        body = self.driver.find_element(by=By.TAG_NAME, value='body')
        body.send_keys(Keys.UP)
        self.pause(2)

    def _find_anchors(self):
        all_anchors = []
        for selector in self.anchor_selectors:
            try:
                print(f'Finding anchors for {selector=}')
                anchors = self.driver.find_elements(*selector)
                all_anchors.extend(anchors)
            except NoSuchElementException as e:
                print(f'NO ADVERTISEMENT ELEMENT: {selector =}')

        return all_anchors

    def _find_advertisements(self):
        all_advertisements = []
        frames = self.driver.find_elements(by=By.TAG_NAME, value='iframe')

        for frame in frames:
            self.driver.switch_to.frame(frame)
            for selector in self.advertisement_selectors:
                try:
                    advertisements = self.driver.find_elements(*selector)
                    all_advertisements.extend(advertisements)
                except NoSuchElementException as e:
                    print(f"NO ELEMENT: {selector = }")

            self.driver.switch_to.default_content()
            if len(all_advertisements) > 8:
                return all_advertisements

        return all_advertisements


if __name__ == '__main__':
    from utils import use_driver

    driver = use_driver()
    driver.get('https://jobcity.pk/')

    bot = BTR(
        driver=driver,
        anchor_selectors=[
            (By.CSS_SELECTOR, ".sidebarjob a"),
            (By.CSS_SELECTOR, ".entry-title a")
        ],
        advertisement_selectors=[
            (By.CSS_SELECTOR, 'a[href*="googleadservice"]'),
            (By.CSS_SELECTOR, 'a[href*="doubleclick"]')
        ]
    )

    bot.start()
    input("ENTER")
    driver.quit()
