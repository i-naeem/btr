
import env
from pprint import pprint
from SearchBot import SearchBot
from SearchEngineConfigs import GOOGLE_CONFIGS
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

service = Service(executable_path=env.CHROME_EXECUTABLE_PATH)
chrome_options = ChromeOptions()
driver = Chrome(service=service, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(5)


google = SearchBot(driver=driver, **GOOGLE_CONFIGS)
search_results = google.search(
    query="site:merjob.com", 
    fltr=lambda el: el.get_attribute('href').lower().find('merjob.com') != -1
)


pprint(search_results)
input("Press enter to quit")