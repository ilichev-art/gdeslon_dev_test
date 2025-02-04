import time

import pytest
from selenium.common import StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from aqa_utils.consts.numeric import N_60, N_5
from aqa_utils.log_util import log

from aqa_ui.selen.driver.driver_container import get_driver as driver


def page_state_is_ready(web_driver):
    try:
        return web_driver.execute_script('return document.readyState') == 'complete'
    except WebDriverException:
        log.error('Error checking page load state:', exc_info=True)
        return False


class Wait:

    @staticmethod
    def until(condition: ec, timeout: int = N_60, log_on_fail: str = 'Failed on waiting for condition'):
        """Wait until the page is fully loaded and condition is met"""
        wait = WebDriverWait(driver(), timeout, ignored_exceptions=[StaleElementReferenceException])
        try:
            return wait.until(condition)
        except TimeoutException:
            pytest.fail(f'TimeoutException: {log_on_fail}')

    @staticmethod
    def until_bool(condition, timeout: int = N_60) -> bool:
        """Wait until a condition is met or timeout is reached, returns bool"""
        wait = WebDriverWait(driver(), timeout, ignored_exceptions=[StaleElementReferenceException])
        try:
            wait.until(condition)
            return True
        except TimeoutException:
            return False

    @staticmethod
    def load_state(timeout: int = N_60):
        """Wait until the page has completely loaded"""
        return Wait.until(page_state_is_ready, timeout)

    @staticmethod
    def sleep(seconds: int = N_5):
        Wait.load_state()
        time.sleep(seconds)
