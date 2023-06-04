from selenium.webdriver.common.by import By
from utils import use_driver, use_proxies
from joblib import delayed, Parallel
from bot import Bot


def main(proxy):
    protocol = proxy.get('protocol')
    server = proxy.get('server')
    port = proxy.get('port')
    uname = "cowrnuzy"
    paswd = "zviptgpzjtmb"

    driver = use_driver(
        username=uname,
        password=paswd,
        proxy_port=port,
        proxy_server=server,
        proxy_protocol=protocol,
    )

    driver.get('https://www.yourfabulouslives.com/')

    bot = Bot(
        driver=driver,
        page_selectors=[(By.CSS_SELECTOR, '.entry-title')],
    )

    try:
        bot.start()
        print("FINISHED")
    except:
        print("FAILED!")

    finally:
        driver.quit()


proxies = use_proxies(max=12)
Parallel(n_jobs=4)(delayed(main)(proxy) for proxy in proxies)
