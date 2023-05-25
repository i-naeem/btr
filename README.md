# BTR - Bot Traffic

> A bot that is used to increased the website traffic using selenium.

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

    - run `python main.py` command.

[python]: https://www.python.org/
[chromebrowser]: https://www.google.com/chrome/
[chromedriver]: https://www.google.com/chrome/
[webshare]: https://webshare.io/
