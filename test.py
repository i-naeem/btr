
import constants
from selenium.webdriver.chrome.service import Service
from undetected_chromedriver import ChromeOptions, Chrome

KEY_DELAY_RANGE = (0.1, 0.2)

PORT = "5074"
SERVER = "2.56.119.93"


service = Service(executable_path=constants.DRIVER_PATH)
chrome_options = ChromeOptions()

chrome_options.add_argument(f'--proxy-server=http://{SERVER}:{PORT}')

driver = Chrome(service=service, options=chrome_options)

driver.implicitly_wait(30)
driver.maximize_window()

driver.get('http://httpbin.org/ip')
input()
