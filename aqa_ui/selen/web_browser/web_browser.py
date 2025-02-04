from typing import List, Optional, Dict

from selenium.common import TimeoutException
from selenium.webdriver.common.print_page_options import PrintOptions

from aqa_ui.selen.driver.driver_container import initialize_driver, get_driver, quit_driver, restart_driver
from aqa_ui.selen.utils.js_executor import JsExecute
from aqa_ui.selen.utils.waiter import Wait
from aqa_utils.consts.numeric import N_5
from aqa_utils.log_util import log


class WebBrowser:

    @staticmethod
    def open(browser: str, width: int or '', height: int or '', remote: bool, hub: str, headless: bool):
        initialize_driver(remote, hub, browser, width, height, headless)

    @staticmethod
    def quit():
        quit_driver()

    @staticmethod
    def restart():
        restart_driver()

    @staticmethod
    def driver():
        return get_driver()

    @staticmethod
    def navigate(url: str):
        get_driver().get(url)
        return WebBrowser.with_load_state()

    @staticmethod
    def execute(script, *args):
        JsExecute.script(script, *args)
        return WebBrowser.with_load_state()

    @staticmethod
    def add_local_storage(key, value):
        JsExecute.script(f'window.localStorage.setItem("{key}", "{value}");')
        return WebBrowser

    @staticmethod
    def delete_local_storage(key):
        JsExecute.script(f'window.localStorage.removeItem("{key}");')
        return WebBrowser

    @staticmethod
    def delete_all_local_storage():
        JsExecute.script('window.localStorage.clear();')
        return WebBrowser

    @staticmethod
    def is_local_storage_presented(key) -> bool:
        return Wait.until_bool(lambda d: JsExecute.script(f"return window.localStorage.getItem('{key}');"), timeout=N_5)

    @staticmethod
    def get_local_storage(key) -> str:
        return Wait.until(lambda d: JsExecute.script(f"return window.localStorage.getItem('{key}');"),
                          log_on_fail=f'Local storage item was not presented: {key}')

    @staticmethod
    def add_cookie(cookie, timeout: int = N_5, retry_count=1):
        try:
            get_driver().add_cookie(cookie)
            name = cookie['name']
            Wait.until(lambda d: d.get_cookie(name),
                       timeout=timeout,
                       log_on_fail=f'Added cookie was not presented: {name}'
                       )
        except TimeoutException as e:
            if retry_count > 0:
                log.warning(
                    f"TimeoutException occurred while adding cookie {cookie['name']}"
                    f" Retrying... Remaining attempts: {retry_count}")
                WebBrowser.add_cookie(cookie, timeout=timeout, retry_count=retry_count - 1)
            else:
                log.error(f"Failed to add cookie '{cookie['name']}' after retries.")
                raise e
        return WebBrowser

    @staticmethod
    def is_cookie_presented(name: str) -> bool:
        return Wait.until_bool(lambda d: d.get_cookie(name), timeout=N_5)

    @staticmethod
    def delete_cookie_named(name: str):
        get_driver().delete_cookie(name)
        return WebBrowser

    @staticmethod
    def delete_all_cookies():
        get_driver().delete_all_cookies()
        return WebBrowser

    @staticmethod
    def get_cookies() -> List[dict]:
        return get_driver().get_cookies()

    @staticmethod
    def get_cookie(name: str) -> Optional[Dict]:
        return get_driver().get_cookie(name)

    @staticmethod
    def back():
        get_driver().back()
        return WebBrowser.with_load_state()

    @staticmethod
    def forward():
        get_driver().forward()
        return WebBrowser.with_load_state()

    @staticmethod
    def refresh():
        get_driver().refresh()
        return WebBrowser.with_load_state()

    @staticmethod
    def close():
        get_driver().close()

    @staticmethod
    def maximize_window():
        get_driver().maximize_window()
        return WebBrowser.with_load_state()

    @staticmethod
    def full_screen_window():
        get_driver().fullscreen_window()
        return WebBrowser.with_load_state()

    @staticmethod
    def minimize_window():
        get_driver().minimize_window()
        return WebBrowser.with_load_state()

    @staticmethod
    def get_pdf(print_options: Optional[PrintOptions] = None):
        return get_driver().print_page(print_options)

    @staticmethod
    def set_script_timeout(seconds: int):
        get_driver().set_script_timeout(seconds)
        return WebBrowser

    @staticmethod
    def set_page_load_timeout(seconds: int):
        get_driver().set_page_load_timeout(seconds)
        return WebBrowser

    @staticmethod
    def set_implicit_wait(seconds: int):
        get_driver().implicitly_wait(seconds)
        return WebBrowser

    @staticmethod
    def get_capabilities() -> dict:
        return get_driver().capabilities

    @staticmethod
    def get_screenshot_as_file(file_name: str):
        """file_name: should end with a `.png` extension"""
        return get_driver().get_screenshot_as_file(file_name)

    @staticmethod
    def set_window_size(width: int, height: int):
        get_driver().set_window_size(width, height)
        return WebBrowser

    @staticmethod
    def with_load_state():
        Wait.load_state()
        return WebBrowser

    @staticmethod
    def with_timeout(timeout: int = N_5):
        Wait.sleep(timeout)
        return WebBrowser
