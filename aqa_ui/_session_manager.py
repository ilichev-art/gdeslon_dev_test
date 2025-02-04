import allure
import pytest

from allure_commons.types import AttachmentType

from aqa_utils.log_util import log
from aqa_ui.selen.driver.driver_container import get_driver, initialize_driver, quit_driver


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome', help='Browser name')
    parser.addoption('--width', action='store', default='', help='Browser width')
    parser.addoption('--height', action='store', default='', help='Browser height')
    parser.addoption('--remote', action='store_true', default=False, help='Run tests in remote mode')
    parser.addoption('--hub', action='store', default='http://selenium-hub:4444/wd/hub', help='Selenium hub')
    parser.addoption('--headless', action='store_true', default=False, help='Run tests in headless mode')


@pytest.fixture
def browser(pytestconfig):
    return pytestconfig.getoption('browser')


@pytest.fixture
def width(pytestconfig):
    return pytestconfig.getoption('width')


@pytest.fixture
def height(pytestconfig):
    return pytestconfig.getoption('height')


@pytest.fixture
def remote(pytestconfig):
    return pytestconfig.getoption('remote')


@pytest.fixture
def hub(pytestconfig):
    return pytestconfig.getoption('hub')


@pytest.fixture
def headless(pytestconfig):
    return pytestconfig.getoption('headless')


@pytest.fixture(scope='session', autouse=True)
def driver_session_config(pytestconfig):
    initialize_driver(
        remote=pytestconfig.getoption('remote'),
        hub=pytestconfig.getoption('hub'),
        browser=pytestconfig.getoption('browser'),
        width=pytestconfig.getoption('width'), height=pytestconfig.getoption('height'),
        headless=pytestconfig.getoption('headless'))
    yield
    quit_driver()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    if result.when == 'call':

        browser = str(item.config.getoption('--browser')).capitalize()
        width = item.config.getoption('--width')
        height = item.config.getoption('--height')

        def __browser():
            if width == '' or height == '':
                return f'{browser} Maximized'
            else:
                return f'{browser} {width} x {height}'

        allure.dynamic.tag(__browser())

        if result.failed:
            try:
                if get_driver() is not None:
                    log.debug(f'Attaching screenshot on fail ...')
                    allure.attach(
                        body=get_driver().get_screenshot_as_png(),
                        name='Screenshot',
                        attachment_type=AttachmentType.PNG
                    )
                    allure.attach(
                        body=get_driver().current_url,
                        name='Url',
                        attachment_type=allure.attachment_type.URI_LIST,
                    )
            except Exception as e:
                log.error(f'Failed to capture screenshot: {str(e)}')
