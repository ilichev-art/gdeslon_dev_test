from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from aqa_utils.consts.numeric import N_1
from aqa_utils.log_util import log

from aqa_ui.selen.driver.driver_container import get_driver as driver
from aqa_ui.selen.utils.waiter import Wait


class Actions:

    @staticmethod
    def get_action_chains():
        return ActionChains(driver())

    @staticmethod
    def drag_and_drop(from_element: WebElement, to_element: WebElement):
        log.debug(f'Performing actions drag and drop action\nFrom {from_element}\nTo {to_element}')
        action = Actions.get_action_chains()
        log.debug('Click and dragg from <-> to')
        action.click_and_hold(from_element).move_to_element(from_element).perform()
        Wait.sleep(N_1)
        log.debug("Performing actions release element")
        action.release(to_element.find_element()).perform()
        Wait.sleep(N_1)

    @staticmethod
    def move_to(element: WebElement):
        log.debug(f'Performing actions hover over element: {element}')
        Actions.get_action_chains().move_to_element(element.find_element()).perform()
        Wait.load_state()

    @staticmethod
    def press(key: str):
        log.debug(f'Performing actions press button: {key}')
        Actions.get_action_chains().send_keys(key).perform()
        Wait.load_state()
