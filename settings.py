from selenium.webdriver.common.by import By

MAX_TRAVERSE = 2
MAX_TABS = 5


DERA_JOBS_PK_DATA = [
    {
        "start_url": "https://duckduckgo.com/?q=site:derajobs.pk",
        "route_selectors": [
            (By.CSS_SELECTOR, '[data-testid="result-title-a"]'),
            (By.CSS_SELECTOR, ".entry-title a"),
            (By.CSS_SELECTOR, ".widget widget_recent_entries li a"),
        ]
    }
]

BLOG_DERA_JOBS_PK_DATA = [
    {
        "source": "DuckDuckGo",
        "start_url": "https://duckduckgo.com/?q=site:blog.derajobs.pk",
        "route_selectors": [
            (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
            (By.CSS_SELECTOR, '[data-testid="result-title-a"]'),
            (By.CSS_SELECTOR, ".entry-title a"),
        ]
    },
    {
        "source": "Bing",
        "start_url": "https://www.bing.com/search?q=site:blog.derajobs.pk",
        "route_selectors": [
            (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
            (By.CSS_SELECTOR, "[aria-label='Search Results'] a[href*='blog.derajobs.pk']"),
            (By.CSS_SELECTOR, ".entry-title a"),

        ]
    },
    {
        "source": "Google Site",
        "start_url": "https://sites.google.com/view/linkedin-business-manager/home",
        "route_selectors": [
            (By.CSS_SELECTOR, ".wp-block-latest-posts__post-title"),
            (By.CSS_SELECTOR, "p[role='presentation'] a"),
            (By.CSS_SELECTOR, ".entry-title a"),
        ]
    },
]
