import env
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service


service = Service(executable_path=env.CHROME_EXECUTABLE_PATH)
chrome_options = ChromeOptions()

driver = Chrome(service=service, options=chrome_options)
driver.maximize_window()
