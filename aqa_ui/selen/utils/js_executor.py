from selenium.common import StaleElementReferenceException, WebDriverException

from aqa_utils.log_util import log

from aqa_ui.selen.driver.driver_container import get_driver as driver
from aqa_ui.selen.utils.waiter import Wait


class JsExecute:

    @staticmethod
    def script(script, *args):
        Wait.load_state()
        try:
            result = driver().execute_script(script, *args)
            Wait.load_state()
            return result
        except StaleElementReferenceException:
            log.warning('StaleElementReferenceException occurred. Retrying execution...', exc_info=True)
            return driver().execute_script(script, *args)
        except WebDriverException as e:
            log.error('WebDriverException caught on JS script execution', exc_info=True)
            raise WebDriverException(f'WebDriverException caught on JS script execution. {e}') from e

    @staticmethod
    def key_press(element, key):
        JsExecute.script("""
        var evt = new KeyboardEvent('keydown', {'key': arguments[1]});
        arguments[0].dispatchEvent(evt);
        """, element, key)

    @staticmethod
    def scroll_into_view(element):
        JsExecute.script("arguments[0].scrollIntoView({block: 'center'});", element)

    @staticmethod
    def force_dom_refresh():
        JsExecute.script("document.documentElement.offsetHeight;")

    @staticmethod
    def get_current_user_agent():
        return JsExecute.script('return navigator.userAgent;')

    @staticmethod
    def get_inner_html_contents():
        return JsExecute.script('return document.body.innerHTML;')

    @staticmethod
    def scroll_to_bottom(max_retries=50, wait_time=1):
        last_height = JsExecute.script('return document.body.scrollHeight')
        retries = 0
        while retries < max_retries:
            JsExecute.script('window.scrollTo(0, document.body.scrollHeight);')
            Wait.sleep(wait_time)

            new_height = JsExecute.script('return document.body.scrollHeight')
            if new_height == last_height:
                break

            last_height = new_height
            retries += 1

        if retries == max_retries:
            log.warning("Reached maximum retries while scrolling to bottom.")
