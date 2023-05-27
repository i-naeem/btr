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
    - Update the proxies list in `proxies.py` file.

4. ### Start the bot

    - run `python main.py` command or start `run.bat` script.

[python]: https://www.python.org/
[webshare]: https://webshare.io/
[chromebrowser]: https://www.google.com/chrome/
[chromedriver]: https://chromedriver.chromium.org/downloads
