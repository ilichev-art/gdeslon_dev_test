from selenium.webdriver.chrome.options import Options

from selenium import webdriver

from aqa_utils.log_util import log


class ChromiumManager:

    @staticmethod
    def _provide_options():
        options = Options()
        options.page_load_strategy = 'eager'
        options.add_argument('--lang=ru')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--log-level=3')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        return options

    class Chrome:

        @staticmethod
        def provide_options():
            return ChromiumManager._provide_options()

        def provide_driver(self, headless: bool):
            options = self.provide_options()
            if headless:
                log.debug('Enabling headless mode')
                options.add_argument('--headless')
            return webdriver.Chrome(options=options)

    class Edge:

        @staticmethod
        def provide_options():
            options = ChromiumManager._provide_options()
            options.set_capability('browserName', 'MicrosoftEdge')
            return options

        def provide_driver(self, headless: bool):
            options = self.provide_options()
            if headless:
                log.debug('Enabling headless mode')
                options.add_argument('--headless')
            return webdriver.Edge(options=options)
