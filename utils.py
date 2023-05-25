from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import time




def scrollToElement(driver:WebDriver, element:WebElement) -> None:
    driver.execute_script("""
function scrollToElement(element) {
  const rect = element.getBoundingClientRect();
  const scrollY = window.scrollY || window.pageYOffset;
  const scrollX = window.scrollX || window.pageXOffset;
  const scrollTargetY = scrollY + rect.top - window.innerHeight / 2;
  const scrollTargetX = scrollX + rect.left - window.innerWidth / 2;
  const duration = 1000;
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
    

def virtual_click(driver:WebDriver, element:WebElement):
    action = ActionChains(driver)
    scrollToElement(driver, element)
    time.sleep(1)
    driver.execute_script('arguments[0].scrollIntoView({block: "center"});', element)
    time.sleep(1)
    action.move_to_element_with_offset(element, 0, 0).perform()
    time.sleep(1)
    action.click().perform()

def scroll_page(driver: WebDriver, speed: float = 1) -> None:
    scroll_height = driver.execute_script("return document.body.scrollHeight")

    # Create an instance of ActionChains
    actions = ActionChains(driver)

    # Perform the scroll action until the end of the page is reached
    while driver.execute_script("return window.pageYOffset + window.innerHeight") < scroll_height:
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(speed)