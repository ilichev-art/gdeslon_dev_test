from typing import Optional

from selenium.common import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

from aqa_utils.consts.numeric import N_60
from aqa_utils.log_util import log

from aqa_ui.selen.driver.driver_factory.driver_provider import Driver

__driver: Optional[WebDriver] = None
__remote: Optional[bool] = None
__hub: Optional[str] = None
__browser: Optional[str] = None
__width: Optional[str] = None
__height: Optional[str] = None
__headless: Optional[bool] = None


def initialize_driver(remote, hub, browser, width, height, headless):
    global __driver, __remote, __hub, __browser, __width, __height, __headless
    try:
        if __driver is None:
            log.debug('Initializing the browser...')
            try:
                __driver = Driver.create_instance(remote=remote, hub=hub, browser=browser, headless=headless)
                __remote = remote
                __hub = hub
                __browser = browser
                __width = width
                __height = height
                __headless = headless
                if width == '' or height == '':
                    __driver.maximize_window()
                else:
                    __driver.set_window_size(width, height)
                __driver.set_script_timeout(N_60)
                __driver.set_page_load_timeout(N_60)
            except WebDriverException as e:
                log.error(f'Failed to initialize WebDriver\n{e}')
                raise WebDriverException(f'Failed to initialize WebDriver. {e}') from e
    except Exception as e:
        log.error(f'An error occurred while configuring the driver: {e}')
        raise Exception(f'WebDriver configuration failed. {e}')

    if __driver is None:
        log.error('Driver not initialized. Please ensure proper initialization')
        raise Exception('Driver initialization failed')


def get_driver() -> Optional[WebDriver]:
    if __driver is None:
        log.error("Driver not initialized. Please ensure proper initialization")
        raise RuntimeError('Driver not initialized')
    return __driver


def quit_driver():
    global __driver
    try:
        if __driver is not None:
            log.debug('Quitting the browser...')
            __driver.quit()
            __driver = None
            log.info('Browser closed')
    except WebDriverException as e:
        log.error(f'Failed to quit the WebDriver cleanly\n{e}')
    except Exception as e:
        log.error(f'An unexpected error occurred during WebDriver teardown\n{e}')
        raise Exception(f'An unexpected error occurred during WebDriver teardown. {e}')


def restart_driver():
    log.debug('Restarting the browser...')
    quit_driver()
    initialize_driver(__remote, __hub, __browser, __width, __height, __headless)
