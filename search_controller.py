from selenium.webdriver.chrome.webdriver import WebDriver;
from selenium.webdriver.common.by import By;
from models import Selector

class SearchController:
    def __init__(self, 
                driver: WebDriver,
                input_selector: Selector = Selector(by=By.CSS_SELECTOR, value="input"),
                search_result_selector: Selector = Selector(by=By.TAG_NAME, value="a"),
                ):
        self.search_result_selector = search_result_selector;
        self.input_selector = input_selector;
        self.search_results = []
        self.driver = driver;
        self._q = None;
    
    
    def search(self, q: str):
        return self.search_results
    
    
    def _find_search_results(self) -> None:
        pass