# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selene import browser
# from dotenv import load_dotenv
# import pytest
#
#
# # Local settings
#
# @pytest.fixture(scope="session", autouse=True)
# def load_env():
#     load_dotenv()
#
# @pytest.fixture(scope='session', autouse=True)
# def browser_management():
#     browser.config.base_url = 'https://gdeslon.kokoc.com'
#     browser.config.timeout = 5
#     browser.config.browser_name = 'chrome'
#     browser.config.window_width = 1900
#     browser.config.window_height = 1080
#
#     driver_options = webdriver.ChromeOptions()
#     browser.config.driver_options = driver_options
#     # driver_options.add_argument('--headless')
#     browser.config.hold_browser_open = True
#
#
#     yield
#
#     browser.quit()


# # Remote settings
import pytest
from dotenv import load_dotenv
import os
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import attach


DEFAULT_BROWSER_VERSION = '100.0'
def pytest_addoption(parser):
    parser.addoption(
        "--browser_version",
        default="100.0"
    )

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function")
def setup_browser(request):
    browser_version = request.config.getoption("--browser_version")
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    options = Options()
    selenoid_capabilities = {
        "browserName": 'chrome',
        "browserVersion": browser_version,
        "selenoid:options": {"enableVideo": True, "enableVNC": True}
    }

    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
        options=options,
    )
    browser.config.driver = driver

    browser.config.base_url = "https://gdeslon.kokoc.com"
    browser.config.window_width = int(os.getenv("selene.window_width", 1920))
    browser.config.window_height = int(os.getenv("selene.window_height", 1080))

    yield browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()

