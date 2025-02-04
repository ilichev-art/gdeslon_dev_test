from aqa_ui.selen.web_page_element.page_element.web_page_element_actionable import WebPageActionableElement
from typing import List


class WebPageElement(WebPageActionableElement):

    def __init__(self, source):
        if isinstance(source, str):
            super().__init__(source)
        elif isinstance(source, WebPageElement):
            super().__init__(source.xpath)
        else:
            raise ValueError('Source must be either a string xpath or another WebElement instance')

    def get_page_elements(self) -> List['WebPageElement']:
        """Intended to be used only on a single subexpression context"""
        return [WebPageElement(self.xpath).of_index_(it + 1) for it in range(len(self._find_elements()))]

    def join_(self, source):
        if isinstance(source, str):
            return WebPageElement(self.xpath + source)
        elif isinstance(source, WebPageElement):
            return WebPageElement(self.xpath + source.xpath)
        else:
            raise ValueError('Source must be either a string xpath or another WebElement instance')

    def or_(self, source):
        if isinstance(source, str):
            xpath = source
        elif isinstance(source, WebPageElement):
            xpath = source.xpath
        else:
            raise ValueError('Source must be either a string xpath or another WebElement instance')
        return WebPageElement(f'{self.xpath} | {xpath}')

    def any_(self):
        return WebPageElement(f'{self.xpath}//*')

    def locator_(self, locator: str):
        return WebPageElement(f'{self.xpath}//{locator}')

    def of_index_(self, index: int):
        """Intended to be used only on a single subexpression context"""
        return WebPageElement(f'({self.xpath})[{index}]')

    def parent_(self):
        return WebPageElement(f'{self.xpath}/..')

    def following_(self, locator: str):
        return WebPageElement(f'{self.xpath}//following::{locator}')

    def following_sibling_(self, locator: str):
        return WebPageElement(f'{self.xpath}/following-sibling::{locator}')

    def preceding_sibling_(self, locator: str):
        return WebPageElement(f'{self.xpath}/preceding-sibling::{locator}')

    def closest_ancestor_(self, xpath: str):
        return WebPageElement(f'{self.xpath}//ancestor::{xpath}')

    def closest_child_(self, xpath: str):
        return WebPageElement(f'{self.xpath}//child::{xpath}')

    def contains_attribute_(self, attribute: str):
        return WebPageElement(f'{self.xpath}[@{attribute}]')

    def contains_attr_with_value_(self, attribute: str, value: str):
        return WebPageElement(f"{self.xpath}[contains(@{attribute}, '{value}')]")

    def contains_(self, content: str):
        return WebPageElement(f'{self.xpath}[contains(., "{content}")]')

    def contains_text_(self, content: str):
        return WebPageElement(f'{self.xpath}[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ",'
                              f' "abcdefghijklmnopqrstuvwxyz"), "{content.lower()}")]')

    def contains_exact_text_(self, content: str):
        return WebPageElement(f'{self.xpath}[normalize-space(text()) = "{content}"]')

    def contains_title_(self, content: str):
        return WebPageElement(f"{self.xpath}[contains(@title, '{content}')]")

    def contains_icon_(self, content: str):
        return WebPageElement(f"{self.xpath}[contains(@icon, '{content}')]")

    def contains_class_(self, content: str):
        return WebPageElement(f"{self.xpath}[contains(@class, '{content}')]")

    def contains_value_(self, content: str):
        return WebPageElement(f"{self.xpath}[contains(@value, '{content}')]")

    def contains_role_(self, content: str):
        return WebPageElement(f"{self.xpath}[contains(@role, '{content}')]")

    def contains_type_(self, content: str):
        return WebPageElement(f"{self.xpath}[contains(@type, '{content}')]")

    def contains_name_(self, content: str):
        return WebPageElement(f"{self.xpath}[contains(@name, '{content}')]")

    def contains_placeholder_(self, content: str):
        return WebPageElement(f"{self.xpath}[contains(@placeholder, '{content}')]")

    def starts_with_(self, content_or_attribute: str, content=None):
        if content is None:
            # If only one argument, it's the content to check against the current node text
            return WebPageElement(f"{self.xpath}[starts-with(., '{content_or_attribute}')]")
        else:
            # If two arguments, the first is the attribute, the second is the content
            return WebPageElement(f"{self.xpath}[starts-with(@{content_or_attribute}, '{content}')]")

    def ends_with_(self, attribute: str, content: str):
        return WebPageElement(
            f"{self.xpath}[substring(@{attribute}, string-length(@{attribute}) - string-length('{content}') + 1)"
            f" = '{content}']")
