from utils import use_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


class SearchController:
    def __init__(self,
                 name: str,
                 driver: WebDriver,

                 start_url=None,
                 results_selector=None,
                 searchbar_selector=None,
                 ):

        self.name = name
        self.driver = driver
        self.start_url = start_url
        self.results_selector = results_selector
        self.searchbar_selector = searchbar_selector

        self.searchbar = None
        self.wait = WebDriverWait(self.driver, 10)

    def search(self, q):
        if self.start_url != self.driver.current_url:
            self.driver.get(self.start_url)

        self.searchbar = self.wait.until(EC.element_to_be_clickable(self.searchbar_selector))
        self.searchbar.send_keys(q, Keys.ENTER)

        search_results = self.wait.until(
            EC.presence_of_all_elements_located(self.results_selector)
        )

        return search_results

    def __str__(self) -> str:
        return f'SearchController[{self.name}]'


if __name__ == '__main__':
    driver = use_driver()

    controller = SearchController(
        name="Google",
        driver=driver,
        start_url="https://google.com",
        searchbar_selector=(By.NAME, 'q'),
        results_selector=(By.XPATH, "//a[h3]")
    )

    try:
        results = controller.search('Hello World')
        for result in results:
            print(result.text)
    except Exception as e:
        print(e)

    input("Press enter to quit.")
    driver.quit()
