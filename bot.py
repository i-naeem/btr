from utils.scrolls import scroll_down, scroll_up
import random

UP = "UP"
DOWN = "DOWN"


class Bot:
    def __init__(self, driver, scroll_speed):
        self.driver = driver
        self.scroll_speed = scroll_speed

        self.anchors = None

    def scroll(self, direction: str = DOWN):
        pass

    def click(self):
        anchor = random.choice(self.anchors)
        anchor.click()
