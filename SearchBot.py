import env
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver


service = Service(executable_path=env.CHROME_EXECUTABLE_PATH)
chrome_options = ChromeOptions()

class SearchBot:
    def __init__(self,
                 name: str,
                 start_url: str,
                 driver: WebDriver,
                 searchbar_selector: str,
                 search_result_selector: str,
                 searchbar_selected_by: By = By.CSS_SELECTOR,
                 search_result_selected_by: By = By.CSS_SELECTOR, 
                 ):
        self.name = name;
        self.driver = driver;
        self.start_url = start_url;
        self.searchbar_selector = searchbar_selector;
        self.searchbar_selected_by = searchbar_selected_by;
        self.search_result_selector = search_result_selector;
        self.search_result_selected_by = search_result_selected_by;
    
    
    def search(self, search_text:str):
        self.driver.get(self.start_url)
            
        searchbar = self.driver.find_element(
            self.searchbar_selected_by, 
            self.searchbar_selector
        )
        
        for char in search_text:
            searchbar.send_keys(char)
        searchbar.send_keys(Keys.ENTER)
        
        search_results = self.driver.find_elements(
            self.search_result_selected_by, 
            self.search_result_selector
        )

        return search_results;
    

if __name__ == "__main__":
    driver = Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(5)
    
    google_bot = SearchBot(
    name="Google",
    driver=driver,
    start_url="https://google.com",
    searchbar_selector="textarea",
    search_result_selector="//a[h3]",
    search_result_selected_by= By.XPATH
    )
    
    search_results = google_bot.search("Hello World")
    
    for index,sr in enumerate(search_results):
        print(f"\n{index}. {sr.text}")

    input("Press enter key to quit")
    driver.quit()
        
        
