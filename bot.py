from utils.scrolls import scroll_down, scroll_up
import random

UP: str = "UP"
DOWN: str = "DOWN"


class Bot:
    def __init__(self, driver, scroll_pause):
        self.driver = driver
        self.scroll_pause = scroll_pause

        self.available_routes = None

    def scroll(self, direction: str = DOWN):
        if direction == DOWN:
            scroll_down(self.driver, self.scroll_pause)
        else:
            scroll_up(self.driver, self.scroll_pause)

    def goto(self):
        route = random.choice(self.available_routes)

        frame = getattr(route, 'iframe', None)
        anchor = getattr(route, 'anchor')

        if frame is not None:  # Check if we clicked or not?
            self.driver.switch_to.frame(frame)
            anchor.click()
        else:
            anchor.click()
