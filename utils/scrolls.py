"""
scrolls.py - Scroll utilities that will be used to scroll the driver.
"""
from selenium.webdriver.remote.webdriver import WebDriver
import time

# Scroll Pixels
SCROLL_PIXEL = 400


def scroll_down(driver: WebDriver, pause: float,) -> None:
    scroll_height = driver.execute_script('return document.body.scrollHeight')
    scroll_speed = SCROLL_PIXEL
    scrolled_pixel = scroll_speed

    while scrolled_pixel < scroll_height:
        driver.execute_script('return window.scrollTo(0, arguments[0])', scrolled_pixel)
        scrolled_pixel = scrolled_pixel + scroll_speed
        time.sleep(pause)


def scroll_up(driver: WebDriver, pause: float) -> None:
    scroll_y = driver.execute_script('return window.scrollY')
    scroll_speed = SCROLL_PIXEL

    while scroll_y > 0:
        driver.execute_script('return window.scrollBy(0, -arguments[0])', scroll_speed)
        scroll_y = scroll_y - scroll_speed
        time.sleep(pause)
