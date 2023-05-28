from selenium.webdriver.remote.webelement import WebElement;
from selenium.webdriver.chrome.webdriver import WebDriver;
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By;
from models import Selector
from typing import List

DEFAULT_SEARCHBAR_SELECTOR = Selector(by=By.CSS_SELECTOR, value="input[type='search']")
DEFAULT_SEARCH_RESULT_SELECTORS = [Selector(by=By.TAG_NAME, value="a")]

class SearchController:
    def __init__(self, 
                driver: WebDriver,
                searchbar_selector: Selector = DEFAULT_SEARCHBAR_SELECTOR,
                search_result_selectors: List[Selector] = DEFAULT_SEARCH_RESULT_SELECTORS,
                ):
        self.search_result_selectors = search_result_selectors;
        self.searchbar_selector = searchbar_selector;
        self.search_results = []
        self.driver = driver;

        self._q = None;
        self._searchbar = None;
    
    
    def search(self, q: str):
        self._find_searchbar();
        self._searchbar.send_keys(q, Keys.ENTER)
        
        return self._find_search_results()
    
    def _find_searchbar(self) -> None:
        self._searchbar = self.driver.find_element(self.searchbar_selector)
    
    def _find_search_results(self) -> List[WebElement]:
        results = []
        for selector in self.search_result_selectors:
            results.extend(self.driver.find_elements(*selector))
        
        return self.search_results;
    


if __name__ == "__main__":
    controller = SearchController(driver=None)