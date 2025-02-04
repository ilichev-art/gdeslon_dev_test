from aqa_utils.log_util import log

from aqa_ui.selen.web_page_element.page_element.web_page_element_provider import provide_web_page_element


class WebPageElementAsserts:

    def __init__(self, xpath: str):
        self._xpath = xpath

    def displayed(self, element_name: str = ''):
        log.debug(f'Asserting page element to be displayed\nElement : {element_name} {self._xpath}')
        if not provide_web_page_element(self._xpath).is_displayed():
            raise AssertionError(f'Expected Page Element to be displayed. Element: {element_name} {self._xpath}')
        return WebPageElementAsserts._PageElementAssertJoiners(self)

    def presented(self, element_name: str = ''):
        log.debug(f'Asserting page element to be presented\nElement : {element_name} {self._xpath}')
        if not provide_web_page_element(self._xpath).is_presented():
            raise AssertionError(f'Expected Page Element to be presented. Element: {element_name} {self._xpath}')
        return WebPageElementAsserts._PageElementAssertJoiners(self)

    def enabled(self, element_name: str = ''):
        log.debug(f'Asserting page element to be enabled\nElement : {element_name} {self._xpath}')
        if not provide_web_page_element(self._xpath).is_enabled():
            raise AssertionError(f'Expected Page Element to be enabled. Element: {element_name} {self._xpath}')
        return WebPageElementAsserts._PageElementAssertJoiners(self)

    def selected(self, element_name: str = ''):
        log.debug(f'Asserting page element to be selected\nElement : {element_name} {self._xpath}')
        if not provide_web_page_element(self._xpath).is_selected():
            raise AssertionError(f'Expected Page Element to be selected. Element: {element_name} {self._xpath}')
        return WebPageElementAsserts._PageElementAssertJoiners(self)

    def contains_attr_with_value(self, attribute: str, value: str, element_name: str = ''):
        log.debug(f'Asserting page element to contain attribute "{attribute}" with value "{value}"'
                  f'\nElement : {element_name} {self._xpath}')
        web_element = provide_web_page_element(self._xpath)
        if not web_element.contains_attr_with_value_(attribute, value).is_presented():
            actual_value = web_element.get_attribute(attribute)
            if actual_value is None or value not in actual_value:
                raise AssertionError(f'Expected Page Element to contain attribute "{attribute}" with value "{value}".'
                                     f' Element: {element_name} {self._xpath}')
        return WebPageElementAsserts._PageElementAssertJoiners(self)

    def contains_attribute(self, attribute: str, element_name: str = ''):
        log.debug(
            f'Asserting page element to contain attribute "{attribute}"\nElement : {element_name} {self._xpath}')
        if not provide_web_page_element(self._xpath).is_attribute_presented(attribute):
            raise AssertionError(
                f'Expected Page Element to contain attribute "{attribute}". Element: {element_name} {self._xpath}')
        return WebPageElementAsserts._PageElementAssertJoiners(self)

    def contains_css_value(self, css_value: str, element_name: str = ''):
        log.debug(
            f'Asserting page element to contain css value "{css_value}"\nElement : {element_name} {self._xpath}')
        if not provide_web_page_element(self._xpath).is_css_value_presented(css_value):
            raise AssertionError(
                f'Expected Page Element to contain css value "{css_value}". Element: {element_name} {self._xpath}')
        return WebPageElementAsserts._PageElementAssertJoiners(self)

    def contains_text(self, text: str, element_name: str = ''):
        log.debug(f'Asserting page element to contain text "{text}"\nElement : {element_name} {self._xpath}')
        actual_text = provide_web_page_element(self._xpath).get_text()
        if text not in actual_text:
            raise AssertionError(
                f'Expected Page Element to contain text "{text}" Actual : {actual_text}'
                f'. Element: {element_name} {self._xpath}')
        return WebPageElementAsserts._PageElementAssertJoiners(self)

    def has_exact_text(self, text: str, element_name: str = ''):
        log.debug(f'Asserting page element text to be "{text}"\nElement : {element_name} {self._xpath}')
        actual_text = provide_web_page_element(self._xpath).get_text()
        if text != actual_text:
            raise AssertionError(
                f'Expected Page Element text to be "{text}" Actual : {actual_text}'
                f'. Element: {element_name} {self._xpath}')
        return WebPageElementAsserts._PageElementAssertJoiners(self)

    def count_exact(self, count: int, element_name: str = ''):
        log.debug(f'Asserting page element count to be "{count}"\nElement : {element_name} {self._xpath}')
        actual_count = provide_web_page_element(self._xpath).get_count()
        if count != actual_count:
            raise AssertionError(
                f'Expected Page Element count to be "{count}" Actual : {actual_count}'
                f'. Element: {element_name} {self._xpath}')
        return WebPageElementAsserts._PageElementAssertJoiners(self)

    def count_exact_or_more(self, count: int, element_name: str = ''):
        log.debug(f'Asserting page element count to be equal or more than "{count}"'
                  f'. Element: {element_name} {self._xpath}')
        actual_count = provide_web_page_element(self._xpath).get_count()
        if actual_count < count:
            raise AssertionError(
                f'Expected Page Element count to be equal or more than "{count}" Actual : {actual_count}'
                f'. Element: {element_name} {self._xpath}')
        return WebPageElementAsserts._PageElementAssertJoiners(self)

    def count_exact_or_less(self, count: int, element_name: str = ''):
        log.debug(f'Asserting page element count to be equal or less than "{count}"'
                  f'\nElement : {element_name} {self._xpath}')
        actual_count = provide_web_page_element(self._xpath).get_count()
        if actual_count > count:
            raise AssertionError(
                f'Expected Page Element count to be equal or less than "{count}" Actual : {actual_count}'
                f'. Element: {element_name} {self._xpath}')
        return WebPageElementAsserts._PageElementAssertJoiners(self)

    def not_(self):
        return WebPageElementAsserts._NegatedPageElementAssert(self)

    class _PageElementAssertJoiners:

        def __init__(self, page_element_assert: 'WebPageElementAsserts'):
            self.__page_element_assert = page_element_assert
            self.__xpath = self.__page_element_assert._xpath

        def and_(self):
            return self.__page_element_assert

        def not_(self):
            return WebPageElementAsserts._NegatedPageElementAssert(self.__page_element_assert)

        def then_(self):
            return provide_web_page_element(self.__xpath)

    class _NegatedPageElementAssert:

        def __init__(self, page_element_assert: 'WebPageElementAsserts'):
            self.__xpath = page_element_assert._xpath
            self.__page_element_assert_joiner = page_element_assert._PageElementAssertJoiners(page_element_assert)
            self.__page_element = provide_web_page_element(self.__xpath)

        def displayed(self, element_name: str = ''):
            log.debug(f'Asserting page element to be not displayed\nElement : {element_name} {self.__xpath}')
            if self.__page_element.is_displayed():
                raise AssertionError(
                    f'Expected Page Element to be not displayed. Element: {element_name} {self.__xpath}')
            return self.__page_element_assert_joiner

        def presented(self, element_name: str = ''):
            log.debug(f'Asserting page element to be not presented\nElement : {element_name} {self.__xpath}')
            if self.__page_element.is_presented():
                raise AssertionError(
                    f'Expected Page Element to be presented. Element: {element_name} {self.__xpath}')
            return self.__page_element_assert_joiner

        def enabled(self, element_name: str = ''):
            log.debug(f'Asserting page element to be not enabled\nElement : {element_name} {self.__xpath}')
            if self.__page_element.is_enabled():
                raise AssertionError(
                    f'Expected Page Element to be not enabled. Element: {element_name} {self.__xpath}')
            return self.__page_element_assert_joiner

        def selected(self, element_name: str = ''):
            log.debug(f'Asserting page element to be not selected\nElement : {element_name} {self.__xpath}')
            if self.__page_element.is_selected():
                raise AssertionError(
                    f'Expected Page Element to be not selected. Element: {element_name} {self.__xpath}')
            return self.__page_element_assert_joiner

        def contains_attr_with_value(self, attribute: str, value: str, element_name: str = ''):
            log.debug(f'Asserting page element to not contain attribute "{attribute}" with value "{value}"'
                      f'\nElement : {element_name} {self.__xpath}')
            web_element = provide_web_page_element(self.__xpath)
            if web_element.contains_attr_with_value_(attribute, value).is_presented():
                actual_value = web_element.get_attribute(attribute)
                if actual_value is not None and value in actual_value:
                    raise AssertionError(
                        f'Expected Page Element to contain attribute "{attribute}" with value "{value}".'
                        f' Element: {element_name} {self.__xpath}')
            return self.__page_element_assert_joiner

        def contains_attribute(self, attribute: str, element_name: str = ''):
            log.debug(
                f'Asserting page element to not contain attribute "{attribute}"'
                f'\nElement : {element_name} {self.__xpath}')
            if self.__page_element.is_attribute_presented(attribute):
                raise AssertionError(
                    f'Expected Page Element to not contain attribute "{attribute}"'
                    f'. Element: {element_name} {self.__xpath}')
            return self.__page_element_assert_joiner

        def contains_css_value(self, css_value: str, element_name: str = ''):
            log.debug(
                f'Asserting page element to not contain css value "{css_value}"'
                f'\nElement : {element_name} {self.__xpath}')
            if self.__page_element.is_css_value_presented(css_value):
                raise AssertionError(
                    f'Expected Page Element to not contain css value "{css_value}"'
                    f'. Element: {element_name} {self.__xpath}')
            return self.__page_element_assert_joiner

        def contains_text(self, text: str, element_name: str = ''):
            log.debug(f'Asserting page element to not contain text "{text}"\nElement : {element_name} {self.__xpath}')
            actual_text = self.__page_element.get_text()
            if text in actual_text:
                raise AssertionError(
                    f'Expected Page Element to not contain text "{text}" Actual : {actual_text}'
                    f'. Element: {element_name} {self.__xpath}')
            return self.__page_element_assert_joiner

        def has_exact_text(self, text: str, element_name: str = ''):
            log.debug(f'Asserting page element text to be not "{text}"\nElement : {element_name} {self.__xpath}')
            actual_text = self.__page_element.get_text()
            if text == actual_text:
                raise AssertionError(
                    f'Expected Page Element text to be not "{text}" Actual : {actual_text}'
                    f'. Element: {element_name} {self.__xpath}')
            return self.__page_element_assert_joiner

        def count_exact(self, count: int, element_name: str = ''):
            log.debug(f'Asserting page element count to be not "{count}"\nElement : {element_name} {self.__xpath}')
            actual_count = self.__page_element.get_count()
            if count == actual_count:
                raise AssertionError(
                    f'Expected Page Element count to be not "{count}" Actual : {actual_count}'
                    f'. Element: {element_name} {self.__xpath}')
            return self.__page_element_assert_joiner
