from typing import List

from selenium.common import StaleElementReferenceException, TimeoutException, ElementNotInteractableException, \
    ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from aqa_utils.log_util import log
from aqa_utils.consts.numeric import N_10, N_3, N_5

from aqa_ui.selen.web_page_element.util.web_page_element_acts import WebPageElementActs
from aqa_ui.selen.web_page_element.util.web_page_element_asserts import WebPageElementAsserts
from aqa_ui.selen.web_page_element.util.web_page_element_js_executes import WebPageElementJsExecutes
from aqa_ui.selen.web_page_element.util.web_page_element_waits import WebPageElementWaits

from aqa_ui.selen.driver.driver_container import get_driver as driver
from aqa_ui.selen.utils.waiter import Wait


class WebPageActionableElement:

    def __init__(self, xpath: str):
        self.xpath = xpath
        self.by = By.XPATH, self.xpath

    def _find_elements(self, timeout=N_10) -> List[WebElement]:
        return self.__apply(lambda: Wait.until(
            ec.presence_of_all_elements_located(self.by),
            timeout,
            f'Element was not detected on the page. Element: {self.xpath}'))

    def find_element(self) -> WebElement:
        return self.__apply(lambda: self._find_elements()[0])

    def is_list_empty(self) -> bool:
        try:
            return self.__apply(
                lambda: len(WebDriverWait(driver(), N_3, ignored_exceptions=[StaleElementReferenceException])
                            .until(ec.presence_of_all_elements_located(self.by))) == 0)
        except TimeoutException:
            log.debug('Element List is empty, return True (is_empty)\nElement : ' + self.xpath)
            return True

    def is_displayed(self) -> bool:
        return not self.is_list_empty() and self.find_element().is_displayed()

    def is_presented(self) -> bool:
        return not self.is_list_empty()

    def is_attribute_presented(self, attribute: str) -> bool:
        return self.find_element().get_attribute(attribute) is not None

    def is_css_value_presented(self, css: str) -> bool:
        return self.find_element().value_of_css_property(css) is not None

    def is_selected(self) -> bool:
        return self.find_element().is_selected()

    def is_enabled(self) -> bool:
        return self.find_element().is_enabled()

    def get_tag_name(self) -> str:
        return self.find_element().tag_name

    def get_attribute(self, attribute: str) -> str | None:
        return self.find_element().get_attribute(attribute)

    def get_css_value(self, css: str) -> str | None:
        return self.find_element().value_of_css_property(css)

    def get_text(self) -> str:
        return self.find_element().text

    def get_all_texts(self) -> List[str]:
        return [element.text for element in self._find_elements()]

    def get_all_class_names(self) -> List[str]:
        return [element.get_attribute('class') for element in self._find_elements()]

    def get_count(self) -> int:
        return len(self._find_elements())

    def get_location(self) -> dict:
        return self.find_element().location

    def get_size(self) -> dict:
        return self.find_element().size

    def get_rect(self) -> dict:
        return self.find_element().rect

    def switch_to_frame(self):
        self.__apply_on_action(lambda: driver().switch_to.frame(self.find_element()))
        return self

    def select(self) -> Select:
        return self.__apply_on_action(lambda: Select(self.find_element()))

    def click(self):
        self.__apply_on_action(lambda: self.wait_until()
                               .displayed(log_on_fail=f'Element was not displayed: {self.xpath}')
                               .and_()
                               .clickable(log_on_fail=f'Element was not clickable: {self.xpath}'))
        try:
            self.__apply(lambda: self.find_element().click())
        except (ElementNotInteractableException, ElementClickInterceptedException):
            log.warning('Element click interception failed, reapplying JS click action')
            self.execute_js().click()
        except TimeoutException as e:
            log.error('Renderer Timedout')
            raise TimeoutException(
                f'Timedout while performing click on displayed and clickable element: {self.xpath}') from e
        return self

    def submit(self):
        self.__apply_on_action(lambda: self.find_element().submit())
        return self

    def send_keys(self, *value: str):
        self.__apply_on_action(lambda: self.find_element().send_keys(*value))
        return self

    def clear(self):
        self.__apply_on_action(lambda: self.find_element().clear())
        return self

    def with_timeout(self, timeout: int = N_5):
        Wait.sleep(timeout)
        return self

    def with_page_load_state(self):
        Wait.load_state()
        return self

    def assert_that(self) -> WebPageElementAsserts:
        return WebPageElementAsserts(self.xpath)

    def wait_until(self) -> WebPageElementWaits:
        return WebPageElementWaits(self.xpath)

    def execute_js(self) -> WebPageElementJsExecutes:
        return WebPageElementJsExecutes(self.xpath, self.find_element())

    def act(self) -> WebPageElementActs:
        return WebPageElementActs(self.xpath, self.find_element())

    def __apply(self, executor, max_retries=5):
        num_retries = 0
        while num_retries < max_retries:
            try:
                Wait.load_state()
                return executor()
            except StaleElementReferenceException:
                log.warning(
                    f'StaleElementReferenceException occurred. '
                    f'Retrying execution (Attempt {num_retries + 1} of {max_retries})')
                num_retries += 1
        raise StaleElementReferenceException(
            f'Could not handle StaleElementReferenceException after {max_retries} retries. Element: ' + self.xpath)

    def __apply_on_action(self, executor):
        self.__apply(lambda: self.execute_js().scroll_into_view())
        return executor()
