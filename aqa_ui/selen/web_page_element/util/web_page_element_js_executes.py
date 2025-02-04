from selenium.webdriver.remote.webelement import WebElement

from aqa_utils.log_util import log

from aqa_ui.selen.utils.js_executor import JsExecute
from aqa_ui.selen.web_page_element.page_element.web_page_element_provider import provide_web_page_element


class WebPageElementJsExecutes:

    def __init__(self, xpath: str, web_element: WebElement):
        self.__xpath = xpath
        self.__web_element = web_element

    def script(self, script, *args):
        JsExecute.script(script, *args)
        return provide_web_page_element(self.__xpath)

    def update_class_value(self, new_value):
        log.debug(f'Executing JS class value update : {new_value}\nElement : {self.__xpath}')
        JsExecute.script('arguments[0].classList.add(arguments[1]);', self.__web_element, new_value)
        return provide_web_page_element(self.__xpath)

    def send_keys(self, value):
        log.debug(f'Executing JS send keys : {value}\nElement : {self.__xpath}')
        JsExecute.script("arguments[0].value=arguments[1];", self.__web_element, value)
        return provide_web_page_element(self.__xpath)

    def click(self):
        log.debug(f'Executing JS click\nElement : {self.__xpath}')
        JsExecute.script("document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE,"
                         " null).singleNodeValue.click();", self.__xpath)
        return provide_web_page_element(self.__xpath)

    def key_press(self, key):
        log.debug(f'Executing JS key press : {key}\nElement : {self.__xpath}')
        JsExecute.key_press(self.__web_element, key)
        return provide_web_page_element(self.__xpath)

    def scroll_into_view(self):
        log.debug(f'Executing JS scroll into view\nElement : {self.__xpath}')
        JsExecute.scroll_into_view(self.__web_element)
        return provide_web_page_element(self.__xpath)

    def get_text(self):
        log.debug(f'Executing JS get text\nElement : {self.__xpath}')
        return JsExecute.script('return arguments[0].textContent;', self.__web_element)

    def is_checked(self):
        log.debug(f'Executing JS is checked\nElement : {self.__xpath}')
        return JsExecute.script('return arguments[0].checked;', self.__web_element)
