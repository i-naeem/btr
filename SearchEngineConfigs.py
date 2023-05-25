from selenium.webdriver.common.by import By

GOOGLE_CONFIGS = {
    "name":"Google",
    "start_url":"https://google.com",
    "searchbar_selector":"textarea",
    "search_result_selector":"//a[h3]",
    "search_result_selected_by": By.XPATH
}

