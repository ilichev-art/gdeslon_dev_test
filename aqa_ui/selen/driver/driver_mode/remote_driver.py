from selenium import webdriver

from aqa_utils.log_util import log

from aqa_ui.selen.driver.browser_manager.chromium_manager import ChromiumManager
from aqa_ui.selen.driver.browser_manager.firefox_manager import FirefoxManager
from aqa_ui.selen.consts.browser_session import chrome, firefox, edge


class RemoteDriver:

    def provide_instance(self, browser: str, hub: str):
        log.info(f'Creating remote browser instance : {browser}')
        options = {
            chrome: ChromiumManager().Chrome().provide_options(),
            edge: ChromiumManager().Edge().provide_options(),
            firefox: FirefoxManager().provide_options(),
        }.get(browser.lower(), None)

        if options is None:
            log.error(f'Browser not supported : {browser}')
            raise ValueError(f'Browser is not supported: {browser}')

        return self.__set_remote(options, hub)

    @staticmethod
    def __set_remote(options, hub):
        return webdriver.Remote(
            command_executor=hub,
            options=options
        )
