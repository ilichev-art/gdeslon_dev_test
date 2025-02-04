from typing import Optional

from selenium.common import NoSuchWindowException

from aqa_ui.selen.utils.js_executor import JsExecute
from aqa_utils.log_util import log

from aqa_ui.selen.driver.driver_container import get_driver as driver
from aqa_ui.selen.utils.waiter import Wait


class WebPageWindowHandles:
    original_window: Optional[str] = None
    new_window: Optional[str] = None

    @staticmethod
    def switch_to_new_window():
        """Switches to a new browser window that is not the current one"""
        WebPageWindowHandles.original_window = driver().current_window_handle
        try:
            all_windows = driver().window_handles
            WebPageWindowHandles.new_window = next(
                window for window in all_windows if window != WebPageWindowHandles.original_window
            )
        except StopIteration:
            raise RuntimeError('No other windows found!')

        driver().switch_to.window(WebPageWindowHandles.new_window)
        driver().maximize_window()
        Wait.load_state()

    @staticmethod
    def switch_to_original_window():
        """Switches focus back to the original window and closes the new window"""
        if WebPageWindowHandles.new_window is None:
            log.error("Attempted to switch to a non-existent new window.")
            raise RuntimeError('New window handle is not set')

        try:
            driver().switch_to.window(WebPageWindowHandles.new_window)
            driver().close()
        except NoSuchWindowException:
            log.warning('The new window is already closed or does not exist')

        driver().switch_to.window(WebPageWindowHandles.original_window)
        driver().switch_to.default_content()

        WebPageWindowHandles.original_window = None
        WebPageWindowHandles.new_window = None
        log.debug('Successfully returned focus to the original window')

    @staticmethod
    def create_new_window():
        """Create new browser window"""
        JsExecute.script("window.open('');")
