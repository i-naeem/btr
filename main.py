from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

CHROME_EXECUTABLE_PATH = "./assets/chromedriver.exe"

service = Service(executable_path=CHROME_EXECUTABLE_PATH)
chrome_options = ChromeOptions()

driver = Chrome(service=service, options=chrome_options)
driver.maximize_window()
