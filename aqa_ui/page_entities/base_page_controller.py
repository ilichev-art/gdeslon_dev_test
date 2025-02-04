import allure

from aqa_utils.consts.numeric import N_5
from aqa_ui.selen.web_browser.web_browser import WebBrowser
from aqa_ui.selen.web_page.page.web_page import WebPage


class BasePageController:
    _web_browser = WebBrowser
    _web_page = WebPage

    @allure.step('Navigate Page')
    def go_to(self, url: str, page_name: str = ''):
        WebPage.navigate(url, page_name)
        return self

    def with_timeout(self, seconds: int = N_5):
        WebPage.with_timeout(seconds)
        return self

    def switch_to_new_window(self):
        WebPage.switch_to_new_window()
        return self

    def switch_to_original_window(self):
        WebPage.switch_to_original_window()
        return self

    def create_new_window(self):
        WebPage.create_new_window()
        return self
