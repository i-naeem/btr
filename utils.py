from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
import time

def virtual_click(driver:WebDriver, element:WebElement):
    action = ActionChains(driver)
    driver.execute_script('arguments[0].scrollIntoView({block: "center"});', element)
    time.sleep(1)
    action.move_to_element_with_offset(element, 0, 0).perform()
    time.sleep(1)
    action.click()