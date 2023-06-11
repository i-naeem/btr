from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
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


def scroll_to_element(driver: WebDriver, element: WebElement) -> None:
    driver.execute_script("""
function scrollToElement(element) {
  const rect = element.getBoundingClientRect();
  const scrollY = window.scrollY || window.pageYOffset;
  const scrollX = window.scrollX || window.pageXOffset;
  const scrollTargetY = scrollY + rect.top - window.innerHeight / 2;
  const scrollTargetX = scrollX + rect.left - window.innerWidth / 2;
  const duration = Math.floor(Math.random() * (2500 - 1000) + 1000)
  const easing = function(t) {
    return t * (2 - t);
  };
  let start;

  if (!scrollTargetY && !scrollTargetX) {
    return;
  }

  window.requestAnimationFrame(function step(timestamp) {
    if (!start) {
      start = timestamp;
    }

    const time = timestamp - start;
    let percent = Math.min(time / duration, 1);
    percent = easing(percent);

    window.scrollTo(
      scrollX + (scrollTargetX - scrollX) * percent,
      scrollY + (scrollTargetY - scrollY) * percent
    );

    if (time < duration) {
      window.requestAnimationFrame(step);
    }
  });
}


element = arguments[0]
scrollToElement(element);""",
                          element)
