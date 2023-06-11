from utils.scrolls import scroll_down, scroll_up
import random

UP = "UP"
DOWN = "DOWN"


class Bot:
    def __init__(self, driver, scroll_pause):
        self.driver = driver
        self.scroll_pause = scroll_pause

        self.anchors = None

    def scroll(self, direction: str = DOWN):
        if direction == DOWN:
            scroll_down(self.driver, self.scroll_pause)
        else:
            scroll_up(self.driver, self.scroll_pause)

    def click(self):
        anchor = random.choice(self.anchors)
        anchor.click()
