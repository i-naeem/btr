
import env
from proxies import PROXIES
from SearchBot import SearchBot
from TrafficBot import TrafficBot
from selenium.webdriver.common.by import By
from SearchEngineConfigs import GOOGLE_CONFIGS
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service


for proxy in PROXIES:
    
    service = Service(executable_path=env.CHROME_EXECUTABLE_PATH)
    chrome_options = ChromeOptions()
    chrome_options.add_argument(f'--proxy-server={proxy.protocol}://{proxy.server}:{proxy.port}')
    driver = Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(5)
    


    def f(el):
        return el.get_attribute('href').lower().find('techwispy.com') != -1

    google = SearchBot(driver=driver, **GOOGLE_CONFIGS)
    search_results = google.search(
        query="site:techwispy.com", 
        fltr=f
    )


    selectors = [
        (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
        (By.CSS_SELECTOR, ".entry-title > a")
    ]

    bot = TrafficBot(
        selectors=selectors,
        pages=search_results,
        driver=driver,
        views=3
    )



    bot.start()

input("Press enter to quit")