from selenium.webdriver.common.by import By
from dataclasses import dataclass
from typing import Tuple
from typing import List


@dataclass
class Site:
    site_name: str
    start_urls: List[Tuple[str, str]]
    search_selectors: List[Tuple[str, str]]
    anchors_selectors: List[Tuple[str, str]]


blog_dera_jobs = Site(
    site_name="BlogDeraJobs",
    start_urls=[
        ("GoogleSite", "https://sites.google.com/view/linkedin-business-manager/home"),
        ("DuckDuckGo", "https://duckduckgo.com/?q=site:https://blog.derajobs.pk"),
        ("Bing", "https://bing.com/?q=site:https://blog.derajobs.pk"),
    ],
    search_selectors=[
        (By.CSS_SELECTOR, 'a[href*="https://blog.derajobs.pk/"]'),
        (By.CSS_SELECTOR, "p[role='presentation'] a")
    ],
    anchors_selectors=[
        (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
        (By.CSS_SELECTOR, ".entry-title a"),
    ]
)
