from selenium.webdriver.support import expected_conditions as ec

from aqa_utils.log_util import log
from aqa_utils.consts.numeric import N_60, N_30

from aqa_ui.selen.driver.driver_container import get_driver as driver
from aqa_ui.selen.utils.waiter import Wait
from aqa_ui.selen.web_page_element.page_element.web_page_element import WebPageElement


class WebPageWaits:

    def all_displayed(self, *elements: WebPageElement):
        log.debug(f'Waiting for elements to be displayed\nElements : {[element.xpath for element in elements]}')
        for element in elements:
            element.wait_until().displayed(N_30, f'Expected element to be displayed. Element: {element.xpath}')
        return WebPageWaits._PageWaitJoiners(self)

    def all_presented(self, *elements: WebPageElement):
        log.debug(f'Waiting for elements to be presented\nElements : {[element.xpath for element in elements]}')
        for element in elements:
            element.wait_until().presented(N_30, f'Expected element to be presented. Element: {element.xpath}')
        return WebPageWaits._PageWaitJoiners(self)

    def url_match(self, pattern: str):
        log.debug(f'Waiting for URL to match pattern "{pattern}"')
        Wait.until(
            ec.url_matches(pattern),
            N_60,
            f'Expected URL to match patter "{pattern}". Actual URL: {driver().current_url}'
        )
        return WebPageWaits._PageWaitJoiners(self)

    def url_contains(self, url_part: str):
        log.debug(f'Waiting for URL to contain "{url_part}"')
        Wait.until(
            ec.url_contains(url_part),
            N_60,
            f'Expected URL to contain "{url_part}". Actual: {driver().current_url}'
        )
        return WebPageWaits._PageWaitJoiners(self)

    def url_is(self, url: str):
        log.debug(f'Waiting for URL to be "{url}"')
        Wait.until(
            ec.url_to_be(url),
            N_60,
            f'Expected URL to be "{url}". Actual: {driver().current_url}'
        )
        return WebPageWaits._PageWaitJoiners(self)

    def title_is(self, title: str):
        log.debug(f'Waiting for title to be "{title}"')
        Wait.until(
            ec.title_is(title),
            N_60,
            f'Expected Title to be "{title}". Actual: {driver().title}')
        return WebPageWaits._PageWaitJoiners(self)

    def title_contains(self, title: str):
        log.debug(f'Waiting for title to contain "{title}"')
        Wait.until(
            ec.title_contains(title)
            , N_60,
            f'Expected Title to contain "{title}". Actual: {driver().title}')
        return WebPageWaits._PageWaitJoiners(self)

    def not_(self):
        return WebPageWaits._NegatedPageWait(self)

    class _PageWaitJoiners:

        def __init__(self, page_wait: 'WebPageWaits'):
            self.__page_wait = page_wait

        def and_(self):
            return self.__page_wait

        def not_(self):
            return WebPageWaits._NegatedPageWait(self.__page_wait)

        def then_(self):
            from ..page.web_page import WebPage
            return WebPage

    class _NegatedPageWait:

        def __init__(self, page_wait: 'WebPageWaits'):
            self.__page_wait = page_wait
            self.__page_wait_joiner = self.__page_wait._PageWaitJoiners(page_wait)

        def all_displayed(self, *elements: WebPageElement):
            log.debug(f'Waiting for elements to be not displayed\nElements : {[element.xpath for element in elements]}')
            for element in elements:
                element.wait_until().not_().displayed(
                    N_30,
                    f'Expected element to be not displayed\nElement: {element.xpath}'
                )
            return self.__page_wait_joiner

        def all_presented(self, *elements: WebPageElement):
            log.debug(f'Waiting for elements to be not presented\nElements : {[element.xpath for element in elements]}')
            for element in elements:
                element.wait_until().not_().presented(
                    N_30,
                    f'Expected element to be not presented\nElement: {element.xpath}'
                )
            return self.__page_wait_joiner

        def url_match(self, pattern: str):
            log.debug(f'Waiting for URL to not match pattern "{pattern}"')
            Wait.until(
                lambda d: not ec.url_matches(pattern)(d),
                N_60,
                f'Expected URL to not match patter "{pattern}". Actual URL: {driver().current_url}'
            )
            return self.__page_wait_joiner

        def url_contains(self, url_part: str):
            log.debug(f'Waiting for URL to not contain "{url_part}"')
            Wait.until(
                lambda d: not ec.url_contains(url_part)(d),
                N_60,
                f'Expected URL to not contain "{url_part}". Actual: {driver().current_url}'
            )
            return self.__page_wait_joiner

        def url_is(self, url: str):
            log.debug(f'Waiting for URL to not be "{url}"')
            Wait.until(
                lambda d: not ec.url_to_be(url)(d),
                N_60,
                f'Expected URL to not be "{url}". Actual: {driver().current_url}'
            )
            return self.__page_wait_joiner

        def title_is(self, title: str):
            log.debug(f'Waiting for title to not be "{title}"')
            Wait.until(
                lambda d: not ec.title_is(title)(d),
                N_60,
                f'Expected Title to not be "{title}". Actual: {driver().title}')
            return self.__page_wait_joiner

        def title_contains(self, title: str):
            log.debug(f'Waiting for title to not contain "{title}"')
            Wait.until(
                lambda d: not ec.title_contains(title)(d),
                N_60,
                f'Expected Title to not contain "{title}". Actual: {driver().title}')
            return self.__page_wait_joiner
