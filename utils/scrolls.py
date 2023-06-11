import time


def scroll_down(driver, pause: float = 0.5) -> None:
    scroll_height = driver.execute_script('return document.body.scrollHeight')
    scroll_speed = 400  # Pixels
    scrolled_pixel = scroll_speed
    while scrolled_pixel < scroll_height:
        driver.execute_script('return window.scrollTo(0, arguments[0])', scrolled_pixel)
        scrolled_pixel = scrolled_pixel + scroll_speed
        time.sleep(pause)


def scroll_up(driver, pause: float = 0.5) -> None:
    scroll_y = driver.execute_script('return window.scrollY')
    scroll_speed = 400

    while scroll_y > 0:
        driver.execute_script('return window.scrollBy(0, -arguments[0])', scroll_speed)
        scroll_y = scroll_y - scroll_speed
        time.sleep(pause)
