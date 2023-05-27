from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from proxies import Proxy
import random
import time


def scrollToElement(driver: WebDriver, element: WebElement) -> None:
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


def virtual_click(driver: WebDriver, element: WebElement):
    action = ActionChains(driver)
    scrollToElement(driver, element)
    time.sleep(random.uniform(1, 2))
    driver.execute_script('arguments[0].scrollIntoView({block: "center"});', element)
    time.sleep(random.uniform(1, 2))
    action.move_to_element_with_offset(element, 0, 0).perform()
    time.sleep(random.uniform(1, 2))
    element.click()


def scroll_up_down(driver: WebDriver, speed: float = 2) -> None:
    scroll_height = driver.execute_script("return document.body.scrollHeight")

    # Create an instance of ActionChains
    actions = ActionChains(driver)

    # Perform the scroll action until the end of the page is reached
    while driver.execute_script("return window.pageYOffset + window.innerHeight") < scroll_height:
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(random.uniform(1, speed))


def get_chrome_options(proxy: Proxy = None, ua: UserAgent = None):
    prefs = {"webrtc.ip_handling_policy": "disable_non_proxied_udp",
             "webrtc.multiple_routes_enabled": False,
             "webrtc.nonproxied_udp_enabled": False, }

    ua = ua if ua else UserAgent().random
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument(f'--user-agent={ua}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-plugins-discovery')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")

    options.add_experimental_option('prefs', prefs)

    if proxy:
        options.add_argument(
            f'--proxy-server={proxy.protocol}://{proxy.server}:{proxy.port}'
        )

    return options
