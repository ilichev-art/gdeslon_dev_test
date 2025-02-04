from aqa_utils.log_util import log

from aqa_ui.selen.driver.driver_container import get_driver as driver


class WebPageAsserts:

    def title_contains(self, title: str):
        log.debug(f'Asserting page title to contain "{title}"')
        actual_title = driver().title
        if title not in actual_title:
            raise AssertionError(f'Expected Page title to contain text "{title}". Actual: {actual_title}')
        return WebPageAsserts._PageAssertJoiners(self)

    def title_is(self, title: str):
        log.debug(f'Asserting page title to be "{title}"')
        actual_title = driver().title
        if title != actual_title:
            raise AssertionError(f'Expected Page Element title to be "{title}". Actual: {actual_title}')
        return WebPageAsserts._PageAssertJoiners(self)

    def url_contains(self, url: str):
        log.debug(f'Asserting page url to contain "{url}"')
        actual_url = driver().current_url
        if url not in actual_url:
            raise AssertionError(f'Expected Page url to contain "{url}". Actual: {actual_url}')
        return WebPageAsserts._PageAssertJoiners(self)

    def url_is(self, url: str):
        log.debug(f'Asserting page url to be "{url}"')
        actual_url = driver().current_url
        if url != actual_url:
            raise AssertionError(f'Expected Page url to be "{url}". Actual: {actual_url}')
        return WebPageAsserts._PageAssertJoiners(self)

    def page_source_contains(self, data: str):
        log.debug(f'Asserting page source to contain "{data}"')
        actual_page_source = driver().page_source
        if data not in actual_page_source:
            raise AssertionError(f'Expected Page source to contain "{data}". Actual: {actual_page_source}')
        return WebPageAsserts._PageAssertJoiners(self)

    def not_(self):
        return WebPageAsserts._NegatedPageAssert(self)

    class _PageAssertJoiners:

        def __init__(self, page_assert: 'WebPageAsserts'):
            self.__page_assert = page_assert

        def and_(self):
            return self.__page_assert

        def not_(self):
            return WebPageAsserts._NegatedPageAssert(self.__page_assert)

        def then_(self):
            from ..page.web_page import WebPage
            return WebPage

    class _NegatedPageAssert:

        def __init__(self, page_assert: 'WebPageAsserts'):
            self.__page_assert = page_assert
            self.__page_assert_joiner = self.__page_assert._PageAssertJoiners(page_assert)

        def title_contains(self, title: str):
            log.debug(f'Asserting page title to not contain "{title}"')
            actual_title = driver().title
            if title in actual_title:
                raise AssertionError(f'Expected Page title to not contain text "{title}". Actual: {actual_title}')
            return self.__page_assert_joiner

        def title_is(self, title: str):
            log.debug(f'Asserting page title to be not "{title}"')
            actual_title = driver().title
            if title == actual_title:
                raise AssertionError(f'Expected Page Element title to be not "{title}". Actual: {actual_title}')
            return self.__page_assert_joiner

        def contains_url(self, url: str):
            log.debug(f'Asserting page url to not contain "{url}"')
            actual_url = driver().current_url
            if url not in actual_url:
                raise AssertionError(f'Expected Page url to not contain "{url}". Actual: {actual_url}')
            return self.__page_assert_joiner

        def url_is(self, url: str):
            log.debug(f'Asserting page url to be not "{url}"')
            actual_url = driver().current_url
            if url == actual_url:
                raise AssertionError(f'Expected Page url to be not "{url}". Actual: {actual_url}')
            return self.__page_assert_joiner

        def page_source_contains(self, data: str):
            log.debug(f'Asserting page source to not contain "{data}"')
            actual_page_source = driver().page_source
            if data in actual_page_source:
                raise AssertionError(f'Expected Page source to not contain "{data}". Actual: {actual_page_source}')
            return self.__page_assert_joiner
