from abc import ABC, abstractmethod

from aqa_ui.selen.web_browser.web_browser import WebBrowser
from aqa_ui.selen.web_page.page.web_page import WebPage


class BasePage(ABC):
    _web_browser = WebBrowser
    _web_page = WebPage

    @abstractmethod
    def assert_loaded(self):
        pass
