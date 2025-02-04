from aqa_utils.log_util import log

from aqa_ui.selen.driver.browser_manager.chromium_manager import ChromiumManager
from aqa_ui.selen.driver.browser_manager.firefox_manager import FirefoxManager
from aqa_ui.selen.consts.browser_session import chrome, firefox, edge


class LocalDriver:

    @staticmethod
    def provide_instance(browser: str, headless: bool):
        log.info(f'Creating local browser instance : {browser}')
        if browser.lower() == chrome:
            return ChromiumManager().Chrome().provide_driver(headless)
        elif browser.lower() == firefox:
            return FirefoxManager().provide_driver(headless)
        elif browser.lower() == edge:
            return ChromiumManager().Edge().provide_driver(headless)
        else:
            log.error(f'Browser not supported : {browser}')
            raise ValueError(f'Browser not supported: {browser}')
