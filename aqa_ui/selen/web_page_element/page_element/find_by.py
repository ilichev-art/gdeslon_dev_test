from aqa_ui.selen.consts.attribute import ID, VALUE, TITLE, NAME, PLACEHOLDER, CLASS, ROLE
from aqa_ui.selen.web_page_element.page_element.web_page_element import WebPageElement


class FindBy:

    @staticmethod
    def xpath(xpath: str):
        return WebPageElement(xpath)

    @staticmethod
    def id(id_value: str):
        return FindBy.attribute_value(ID, id_value)

    @staticmethod
    def partial_id(id_part: str):
        return FindBy.attribute_partial_value(ID, id_part)

    @staticmethod
    def value(value: str):
        return FindBy.attribute_value(VALUE, value)

    @staticmethod
    def partial_value(value_part: str):
        return FindBy.attribute_partial_value(VALUE, value_part)

    @staticmethod
    def title(title: str):
        return FindBy.attribute_value(TITLE, title)

    @staticmethod
    def partial_title(title_part: str):
        return FindBy.attribute_partial_value(TITLE, title_part)

    @staticmethod
    def name(name: str):
        return FindBy.attribute_value(NAME, name)

    @staticmethod
    def partial_name(name_part: str):
        return FindBy.attribute_partial_value(NAME, name_part)

    @staticmethod
    def placeholder(placeholder: str):
        return FindBy.attribute_value(PLACEHOLDER, placeholder)

    @staticmethod
    def partial_placeholder(placeholder_part: str):
        return FindBy.attribute_partial_value(PLACEHOLDER, placeholder_part)

    @staticmethod
    def class_name(class_name: str):
        return FindBy.attribute_value(CLASS, class_name)

    @staticmethod
    def partial_class_name(class_name_part: str):
        return FindBy.attribute_partial_value(CLASS, class_name_part)

    @staticmethod
    def role(role: str):
        return FindBy.attribute_value(ROLE, role)

    @staticmethod
    def partial_role(role_part: str):
        return FindBy.attribute_partial_value(ROLE, role_part)

    @staticmethod
    def locator(locator: str):
        return WebPageElement(f'//{locator}')

    @staticmethod
    def text(text: str):
        return WebPageElement(f"//*[text()='{text}']")

    @staticmethod
    def partial_text(partial_text: str):
        return WebPageElement(f"//*[contains(text(), '{partial_text}')]")

    @staticmethod
    def exact_match(locator: str, attribute: str, value: str):
        return WebPageElement(f"//{locator}[@{attribute}='{value}']")

    @staticmethod
    def partial_match(locator: str, attribute: str, value_part: str):
        return WebPageElement(f"//{locator}[contains(@{attribute}, '{value_part}')]")

    @staticmethod
    def attribute_value(attribute: str, value: str):
        return WebPageElement(f"//*[@{attribute}='{value}']")

    @staticmethod
    def attribute_partial_value(attribute: str, value_part: str):
        return WebPageElement(f"//*[contains(@{attribute}, '{value_part}')]")
