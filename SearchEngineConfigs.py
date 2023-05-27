from selenium.webdriver.common.by import By

GOOGLE_CONFIGS = {
    "name": "Google",
    "start_url": "https://google.com",
    "searchbar_selector": "textarea",
    "search_result_selector": "//a[h3]",
    "search_result_selected_by": By.XPATH,
}

BING_CONFIGS = {
    "name": "Bing",
    "start_url": "https://bing.com",
    "searchbar_selector": "#sb_form_q",
    "search_result_selector": ".b_algo > h2 > a",
}

DUCKDUCKGO = {
    "start_url": "https://duckduckgo.com",
    "name": "DuckDuckGo",
    "searchbar_selector": "input[aria-label='Search with DuckDuckGo']",
    "search_result_selector": "article[data-testid='result'] h2 > a",
}
