from aqa_ui.selen.utils.waiter import Wait


def provide_web_page_element(xpath: str):
    from aqa_ui.selen.web_page_element.page_element.web_page_element import WebPageElement
    Wait.load_state()
    return WebPageElement(xpath)
