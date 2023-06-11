# How to use the bot? Step by Step instructions

1. Setup up the bot see `README.md`
2. Goto Settings File
3. Set the `MAX_TABS` to set the max tab to open on chrome.
4. Set the `MAX_TRAVERSE` to how many time the bot will traverse.
5. Add your site data in the following format

    ```py
    YOUR_SITE_DATA = [
      {
        "source": "Give this data a suitable name maybe this link",
        "start_url": "The first page selenium will open",
        "route_selectors": [ 
          #The selectors which will be used to find more pages on the site.
          (By.CSS_SELECTOR, '.my-page-anchor-class')
        ]
      }
    ]
    ```

6. Now go to 2nd line of `main` function in `__main__.py` file and modified the following line

    ```diff
    - data = random.choice(settings.BLOG_DERA_JOBS_PK_DATA)

    + data = random.choice(settings.YOUR_SITE_DATA)
    ```

7. Run the script `py .` or `py __main__.py`.
