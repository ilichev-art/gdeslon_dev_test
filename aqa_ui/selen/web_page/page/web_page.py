from selenium.common import InvalidArgumentException, WebDriverException

from aqa_utils.log_util import log
from aqa_utils.consts.numeric import N_5
from aqa_ui.selen.web_page.util.web_page_waits import WebPageWaits

from aqa_ui.selen.driver.driver_container import get_driver as driver
from aqa_ui.selen.utils.actions import Actions
from aqa_ui.selen.utils.js_executor import JsExecute
from aqa_ui.selen.utils.waiter import Wait
from aqa_ui.selen.web_page.util.web_page_asserts import WebPageAsserts
from aqa_ui.selen.web_page.util.web_page_window_handles import WebPageWindowHandles
from aqa_ui.selen.web_page_element.page_element.web_page_element import WebPageElement
from aqa_ui.selen.web_page_element.page_element.find_by import FindBy


class WebPage:

    @staticmethod
    def driver():
        return driver()

    @staticmethod
    def assert_that() -> WebPageAsserts:
        return WebPageAsserts()

    @staticmethod
    def wait_until() -> WebPageWaits:
        return WebPageWaits()

    @staticmethod
    def wait():
        return Wait

    @staticmethod
    def execute_js():
        return JsExecute

    @staticmethod
    def act():
        return Actions

    @staticmethod
    def navigate(url: str, page_name: str = ''):
        log.info(f"Navigating to : {page_name} {url}")
        try:
            driver().get(url)
            Wait.load_state()
            return WebPage
        except InvalidArgumentException as e:
            log.error(f'Invalid param Base Url : {url}', exc_info=True)
            raise InvalidArgumentException(f'Invalid param Base Url: {url}') from e
        except WebDriverException as ex:
            log.error(f'Target destination is not reachable : {url}', exc_info=True)
            raise WebDriverException(f'Target destination is not reachable: {url}') from ex

    @staticmethod
    def with_timeout(timeout: int = N_5):
        Wait.sleep(timeout)
        return WebPage

    @staticmethod
    def with_page_load_state():
        Wait.load_state()
        return WebPage

    @staticmethod
    def refresh():
        log.debug('Refreshing the page')
        driver().refresh()
        Wait.load_state()
        return WebPage

    @staticmethod
    def get_url():
        return driver().current_url

    @staticmethod
    def get_title():
        return driver().title

    @staticmethod
    def get_page_source():
        return driver().page_source

    @staticmethod
    def get_body_element():
        return FindBy.locator('body')

    @staticmethod
    def switch_to_iframe(element: WebPageElement):
        log.debug(f'Switching to frame\nElement : {element.xpath}')
        driver().switch_to.frame(element.find_element())
        return WebPage

    @staticmethod
    def switch_back_from_iframe():
        log.debug('Switching to default content')
        driver().switch_to.default_content()
        return WebPage

    @staticmethod
    def switch_to_new_window():
        log.debug('Switching to the new window')
        WebPageWindowHandles.switch_to_new_window()
        return WebPage

    @staticmethod
    def switch_to_original_window():
        log.debug('Switching to the original window')
        WebPageWindowHandles.switch_to_original_window()
        return WebPage

    @staticmethod
    def create_new_window():
        log.debug('Creating new window')
        WebPageWindowHandles.create_new_window()
        return WebPage
