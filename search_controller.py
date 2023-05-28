from selenium.webdriver.chrome.service import Service
from undetected_chromedriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dataclasses import astuple
from models import Selector
from typing import List
import utils


DEFAULT_SEARCHBAR_SELECTOR = Selector(by=By.NAME, value="q")
DEFAULT_SEARCH_RESULT_SELECTORS = [Selector(by=By.TAG_NAME, value="a")]


class SearchController:
    def __init__(self,
                 driver: WebDriver,
                 searchbar_selector: Selector = DEFAULT_SEARCHBAR_SELECTOR,
                 search_result_selectors: List[Selector] = DEFAULT_SEARCH_RESULT_SELECTORS,
                 ):
        self.search_result_selectors = search_result_selectors
        self.searchbar_selector = searchbar_selector
        self.driver = driver

        self._q = None
        self._searchbar = None
        self.search_results = []

    def search(self, q: str):
        self._q = q
        self._find_searchbar()

        utils.logger.info('SearchController: Searching query keywords')

        self._searchbar.send_keys(q, Keys.ENTER)

        return self._find_search_results()

    def _find_searchbar(self) -> None:
        utils.logger.info(f'SearchController: Searching for searchbar')

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(astuple(self.searchbar_selector))
        )

        self._searchbar = self.driver.find_element(
            self.searchbar_selector.by, self.searchbar_selector.value
        )

    def _find_search_results(self) -> List[WebElement]:
        utils.logger.info(f'SearchController: Searching for search results')

        for selector in self.search_result_selectors:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_any_elements_located(*astuple(selector))
                )
                results = self.driver.find_elements(*astuple(selector))
                self.search_results.extend(results)
            except:
                pass

        utils.logger.info(f'SearchController: Found {len(self.search_results)} Search Result(s)')

        if len(self.search_results) == 0:
            raise Exception("Could not find any links to open...")

        return self.search_results


if __name__ == "__main__":
    driver = Chrome(service=Service(executable_path='./assets/chromedriver.exe'))
    driver.maximize_window()
    driver.get('https://bing.com')
    controller = SearchController(driver=driver,
                                  search_result_selectors=[
                                      Selector(by=By.CSS_SELECTOR, value="h2 > a")
                                  ]
                                  )

    for item in controller.search('Hello World'):
        print(item.text)
