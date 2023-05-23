from selenium.webdriver.chrome.service import Service
from undetected_chromedriver import Chrome

DRIVER_PATH = "./files/chromedriver.exe"


service = Service(executable_path=DRIVER_PATH)
driver = Chrome(service=service)
