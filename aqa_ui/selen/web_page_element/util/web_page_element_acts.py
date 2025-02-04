from selenium.webdriver.remote.webelement import WebElement

from aqa_utils.log_util import log

from aqa_ui.selen.utils.actions import Actions
from aqa_ui.selen.web_page_element.page_element.web_page_element_provider import provide_web_page_element


class WebPageElementActs:

    def __init__(self, xpath: str, web_element: WebElement):
        self.xpath = xpath
        self.web_element = web_element

    def hover_over(self):
        log.debug(f'Performing actions hover over\nElement : {self.xpath}')
        Actions.get_action_chains().move_to_element(self.web_element).perform()
        return provide_web_page_element(self.xpath)

    def send_keys(self, keys):
        """Send keys to the active element"""
        log.debug(f'Performing actions Send keys : {keys}\nElement : {self.xpath}')
        Actions.get_action_chains().send_keys(keys).perform()
        return provide_web_page_element(self.xpath)

    def double_click(self):
        log.debug(f'Performing actions double click\nElement : {self.xpath}')
        Actions.get_action_chains().double_click(self.web_element).perform()
        return provide_web_page_element(self.xpath)

    def click_and_hold(self):
        log.debug(f'Performing actions click and hold\nElement : {self.xpath}')
        Actions.get_action_chains().click_and_hold(self.web_element).perform()
        return provide_web_page_element(self.xpath)

    def release(self):
        log.debug(f'Performing actions release\nElement : {self.xpath}')
        Actions.get_action_chains().release(self.web_element).perform()
        return provide_web_page_element(self.xpath)

    def key_up(self, value: str):
        """Send key to the active element"""
        log.debug(f'Performing actions key UP : {value}\nElement : {self.xpath}')
        Actions.get_action_chains().key_up(value, self.web_element).perform()
        return provide_web_page_element(self.xpath)

    def key_down(self, value: str):
        """Send key to the active element"""
        log.debug(f'Performing actions key DOWN : {value}\nElement : {self.xpath}')
        Actions.get_action_chains().key_down(value, self.web_element).perform()
        return provide_web_page_element(self.xpath)
