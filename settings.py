from selenium.webdriver.common.by import By

MIN_TIME_PAUSE = 2
MAX_TIME_PAUSE = 3
MAX_TRAVERSE = 3
MAX_TABS = 3


DERA_JOBS_PK_DATA = [
    {
        "start_url": "https://duckduckgo.com/?q=site:derajobs.pk",
        "route_selectors": [
            (By.CSS_SELECTOR, ".result-title-a"),
            (By.CSS_SELECTOR, ".entry-title a"),
            (By.CSS_SELECTOR, ".widget widget_recent_entries li a"),
        ]
    }
]

BLOG_DERA_JOBS_PK_DATA = [
    {
        "start_url": "https://duckduckgo.com/?q=site:blog.derajobs.pk",
        "route_selectors": [
            (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
            (By.CSS_SELECTOR, ".result-title-a"),
            (By.CSS_SELECTOR, ".entry-title a"),
        ]
    },
    {
        "start_url": "https://sites.google.com/view/linkedin-business-manager/home",
        "route_selectors": [
            (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
            (By.CSS_SELECTOR, "p[role='presentation'] a"),
            (By.CSS_SELECTOR, ".entry-title a"),
        ]
    },
]
