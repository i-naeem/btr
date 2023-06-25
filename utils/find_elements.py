"""
find_elements.py - Elements finder utilities.
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from typing import List
import random


def find_by_selectors(
    timeout: int,
    max_element: int,
    driver: WebDriver,
    selectors: List[WebElement],
    randomize_elements: bool = True
):

    wait = WebDriverWait(driver, timeout)

    all_elements = []
    for selector in selectors:
        if len(all_elements) > max_element:
            break
        try:
            elements = wait.until(EC.presence_of_all_elements_located(selector))
            all_elements.extend(elements)
        except TimeoutException as e:
            print('TIMEOUT')

    if randomize_elements:
        random.shuffle(all_elements)

    return all_elements
