from selenium.webdriver.firefox.options import Options

from selenium import webdriver

from aqa_utils.log_util import log


class FirefoxManager:

    def provide_driver(self, headless: bool):
        options = self.provide_options()
        if headless:
            log.debug('Enabling headless mode')
            options.add_argument('--headless')
        return webdriver.Firefox(options=options)

    @staticmethod
    def provide_options():
        options = Options()
        options.set_preference('webdriver.load.strategy', 'eager')
        options.set_preference('intl.accept_languages', 'ru')
        options.accept_insecure_certs = True
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        return options
