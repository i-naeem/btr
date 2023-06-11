from selenium.webdriver.chrome.service import Service
from seleniumwire.undetected_chromedriver import ChromeOptions, Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def use_driver():
    s = Service(executable_path='./assets/chromedriver.exe')
    o = ChromeOptions()
    so = dict()

    return Chrome(service=s, options=o, seleniumwire_options=so)


def find_by_selectors(driver, selectors, timeout=2, max_element=5):
    wait = WebDriverWait(driver, timeout)

    all_elements = []
    for selector in selectors:
        if len(all_elements) > max_element:
            return all_elements
        try:
            elements = wait.until(EC.presence_of_all_elements_located(selector))
            all_elements.extend(elements)
        except TimeoutException as e:
            print(f'TIMEOUT: [{selector}]')

    if len(all_elements) == 0:
        raise NoSuchElementException(msg="There is no element present for your selector.")

    return all_elements
