# BTR - Bot Traffic

> A python bot that uses selenium to increase traffic the websites.
> The bot opens the different search engines enter the users query and search for the users website.
> It then opens one of the links from different links from search results and views different pages.

## Requirements

- [Python 3.8+][python]
- [Chrome Browser][chromebrowser]
- Windows

## Instruction

0. ### Python and Packages Installation

    - [Download][python] and Install Python
    - run `set-env.bat` command.

1. ### Download Chrome Driver

    - Install [Chrome Browser][chromebrowser]
    - [Download Chrome Driver][chromedriver] _the driver should match with chrome version_.
    - Create `assets` folder
    - Extract the [Chrome Driver][chromedriver] to extract folder

2. ### Setup Chromium Path

    - Create `.env` file.
    - Add following line `CHROME_EXECUTABLE_PATH="./assets/chromedriver.exe"`.

3. ### Proxies

    - Goto [WebShare.io][webshare]
    - Create an account.
    - Add the proxies in `./assets/proxies.json` file.

4. ### Start the bot

    - run `python main.py` command.

5. ### Configurations

    - `q` refers to the query that would be search on duckduckgo
    - `max_views` refers to the max tab that will be open at once
    - `max_traverse` refers to maximum traversal of pages like for example we open 5 pages in one iteration that once traverse in second traverse we will select a random open tab and open another `max_tabs` and so on.

> NOTE: The bot is still in development and I'll probably make it more easy and efficient to configure it but if you wanna test you'd have to bear this for moment.

[python]: https://www.python.org/
[webshare]: https://webshare.io/
[chromebrowser]: https://www.google.com/chrome/
[chromedriver]: https://chromedriver.chromium.org/downloads
