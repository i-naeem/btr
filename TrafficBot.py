import time
import random
from typing import List, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

class TrafficBot:
    def __init__(self,
                 selectors: List[Tuple[By, str]],
                 anchors: List[WebElement], 
                 driver: WebDriver,
                 views: int = 5
    ):
        self.views = views
        self.driver = driver
        self.selectors = selectors
        self.anchors =  anchors if anchors else []
        
    @property
    def isAnchorsEmpty(self):
        return bool(len(self.anchors))

    def start(self) -> None:
        if self.isAnchorsEmpty:
            print('There are no pages found the page to view more.')
            return None
        
        else:
            for _ in range(self.views):
                anchor = random.choice(self.anchors)
                self.view_page(anchor)
    
    def view_page(self, anchor: WebElement) -> None:
        anchor.click()
        time.sleep(3)
        current_page_anchors = []
        
        for selector in self.selectors:
            items = self.driver.find_elements(*selector)
            current_page_anchors.extend(items)
            
        self.anchors = current_page_anchors
        
        return None
        # Scroll up and down
        # Gather all the available links from the page
        # Update available_pages
        
        
        
    