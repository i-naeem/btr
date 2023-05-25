import env
from SearchBot import SearchBot
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service


service = Service(executable_path=env.CHROME_EXECUTABLE_PATH)

chrome_options = ChromeOptions()
driver = Chrome(service=service, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(5)

google = SearchBot(
    name="Google",
    driver=driver,
    start_url="https://google.com",
    searchbar_selector="textarea",
    search_result_selector="//a[h3]",
    search_result_selected_by= By.XPATH
    )

