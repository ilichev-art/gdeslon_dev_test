from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from aqa_utils.consts.numeric import N_30, N_15
from aqa_utils.log_util import log

from aqa_ui.selen.utils.waiter import Wait
from aqa_ui.selen.web_page_element.page_element.web_page_element_provider import provide_web_page_element


class WebPageElementWaits:

    def __init__(self, xpath: str):
        self._xpath = xpath
        self._by = By.XPATH, self._xpath

    def clickable(self, wait: int = N_30, log_on_fail: str = ''):
        log.debug(f'Waiting for being clickable\nElement : {self._xpath}')
        Wait.until(ec.element_to_be_clickable(self._by), wait, log_on_fail)
        return WebPageElementWaits._PageElementAssertJoiners(self)

    def selected(self, wait: int = N_30, log_on_fail: str = ''):
        log.debug(f'Waiting for being selected\nElement : {self._xpath}')
        Wait.until(ec.element_located_to_be_selected(self._by), wait, log_on_fail)
        return WebPageElementWaits._PageElementAssertJoiners(self)

    def displayed(self, wait: int = N_30, log_on_fail: str = ''):
        log.debug(f'Waiting for being displayed\nElement : {self._xpath}')
        Wait.until(ec.visibility_of_element_located(self._by), wait, log_on_fail)
        return WebPageElementWaits._PageElementAssertJoiners(self)

    def presented(self, wait: int = N_30, log_on_fail: str = ''):
        log.debug(f'Waiting for being presented\nElement : {self._xpath}')
        Wait.until(ec.presence_of_element_located(self._by), wait, log_on_fail)
        return WebPageElementWaits._PageElementAssertJoiners(self)

    def text_presented(self, text: str, wait: int = N_30, log_on_fail: str = ''):
        log.debug(f'Waiting for text being presented\nElement : {self._xpath}')
        Wait.until(ec.text_to_be_present_in_element(self._by, text_=text), wait, log_on_fail)
        return WebPageElementWaits._PageElementAssertJoiners(self)

    def attribute_text_presented(self, attribute: str, text: str, wait: int = N_30, log_on_fail: str = ''):
        log.debug(f'Waiting for attribute text being presented\nElement : {self._xpath}')
        Wait.until(ec.text_to_be_present_in_element_attribute(self._by, attribute_=attribute, text_=text), wait,
                   log_on_fail)
        return WebPageElementWaits._PageElementAssertJoiners(self)

    def attribute_presented(self, attribute: str, wait: int = N_30, log_on_fail: str = ''):
        log.debug(f'Waiting for attribute being presented\nElement : {self._xpath}')
        Wait.until(ec.element_attribute_to_include(self._by, attribute_=attribute), wait, log_on_fail)
        return WebPageElementWaits._PageElementAssertJoiners(self)

    def not_(self):
        return WebPageElementWaits._NegatedPageElementWait(self)

    class _PageElementAssertJoiners:

        def __init__(self, page_element_wait: 'WebPageElementWaits'):
            self.__page_element_wait = page_element_wait
            self.__xpath = self.__page_element_wait._xpath

        def and_(self):
            return self.__page_element_wait

        def not_(self):
            return WebPageElementWaits._NegatedPageElementWait(self.__page_element_wait)

        def then_(self):
            return provide_web_page_element(self.__xpath)

    class _NegatedPageElementWait:

        def __init__(self, page_element_wait: 'WebPageElementWaits'):
            self.__xpath = page_element_wait._xpath
            self.__by = page_element_wait._by
            self.__page_element_assert_joiner = page_element_wait._PageElementAssertJoiners(page_element_wait)
            self.__page_element = provide_web_page_element(self.__xpath)

        def selected(self, wait: int = N_15, log_on_fail: str = ''):
            log.debug(f'Waiting for being not selected\nElement : {self.__xpath}')
            Wait.until(lambda driver: not self.__page_element.is_selected(), wait, log_on_fail)
            return self.__page_element_assert_joiner

        def displayed(self, wait: int = N_15, log_on_fail: str = ''):
            log.debug(f'Waiting for being not displayed\nElement : {self.__xpath}')
            Wait.until(ec.invisibility_of_element_located(self.__by), wait, log_on_fail)
            return self.__page_element_assert_joiner

        def presented(self, wait: int = N_15, log_on_fail: str = ''):
            log.debug(f'Waiting for being not presented\nElement : {self.__xpath}')
            Wait.until(lambda driver: not self.__page_element.is_presented(), wait, log_on_fail)
            return self.__page_element_assert_joiner

        def text_presented(self, text: str, wait: int = N_15, log_on_fail: str = ''):
            log.debug(f'Waiting for text being not presented\nElement : {self.__xpath}')
            Wait.until(lambda driver: self.__page_element.get_text() != text, wait, log_on_fail)
            return self.__page_element_assert_joiner

        def attribute_text_presented(self, attribute: str, text: str, wait: int = N_15, log_on_fail: str = ''):
            log.debug(f'Waiting for attribute text being presented\nElement : {self.__xpath}')
            Wait.until(lambda driver: text not in self.__page_element.get_attribute(attribute), wait, log_on_fail)
            return self.__page_element_assert_joiner

        def attribute_presented(self, attribute: str, wait: int = N_15, log_on_fail: str = ''):
            log.debug(f'Waiting for attribute being not presented\nElement : {self.__xpath}')
            Wait.until(lambda driver: not self.__page_element.is_attribute_presented(attribute), wait, log_on_fail)
            return self.__page_element_assert_joiner
