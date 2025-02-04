from abc import abstractmethod
from typing import Union, List

import allure
from aqa_ui.page_entities.base_page import BasePage
from aqa_ui.selen.web_page_element.page_element.find_by import FindBy
from aqa_ui.selen.web_page_element.page_element.web_page_element import WebPageElement
from aqa_utils.log_util import log


class BaseDataTable(BasePage):
    def __init__(self, parent_table: WebPageElement):
        self.parent_table = parent_table
        self.head = self.parent_table.join_(FindBy.locator('thead')).join_(FindBy.locator('tr'))
        self.head_cell = self.head.join_(FindBy.locator('th'))
        self.body = parent_table.join_(FindBy.locator('tbody'))
        self.body_row = self.body.join_(FindBy.locator('tr'))
        self.row_cell_td = self.body_row.join_(FindBy.locator('td'))
        self.row_cell_th = self.body_row.join_(FindBy.locator('th'))

    @abstractmethod
    def get_entry(self):
        pass

    @allure.step('Assert Results Data Table display')
    def assert_loaded(self):
        log.info('Assert Results Data Table to display')
        self._web_page.wait_until().all_displayed(self.parent_table, self.head, self.body)
        return self

    def get_all_entry_elements(self, entry: str = None):
        return self.__entry(entry=entry).get_all()

    def get_entries_size(self) -> int:
        return self.__entry().size()

    def has_entry(self, entry: Union[int, str] = None) -> bool:
        return self.__entry(entry).is_presented()

    def assert_has_entry(self, entry: Union[int, str] = None):
        self._web_page.wait().until(lambda d: self.__entry(entry).get_all() != [])

    def __entry(self, entry: Union[int, str] = None):
        return BaseDataTableEntry(parent_table_ini=self, entry=entry)


class BaseDataTableEntry:
    def __init__(self, parent_table_ini, entry):
        self.parent_table_ini = parent_table_ini
        if isinstance(entry, str):
            self.entry_element = parent_table_ini.row_cell_td.contains_(f'{entry}') \
                .or_(parent_table_ini.row_cell_th.contains_(f'{entry}')).of_index_(1).closest_ancestor_('tr')
        elif isinstance(entry, int):
            self.entry_element = parent_table_ini.body_row.of_index_(entry)
        else:
            self.entry_element = parent_table_ini.body_row

    def get_header_cell_by_name(self, entry_name: str) -> int:
        return self.parent_table_ini.head_cell.get_all_texts().index(entry_name) + 1

    def get_body_cell_value_by_index(self, index: int) -> str:
        return self.entry_element.join_('/*').of_index_(index).get_text()

    def get_body_cell_element_by_index(self, index: int) -> WebPageElement:
        return self.entry_element.join_('/*').of_index_(index)

    def get_column_cell_element(self, column_cell):
        try:
            index = self.get_header_cell_by_name(column_cell)
        except KeyError:
            raise ValueError(f'Column {column_cell} does not exist')
        try:
            return self.get_body_cell_element_by_index(index)
        except IndexError:
            raise ValueError(f'Rows have changed or the column index {index} is invalid for {column_cell}')

    def get_all(self) -> List[WebPageElement]:
        return self.entry_element.get_page_elements()

    def is_displayed(self) -> bool:
        return self.entry_element.is_displayed()

    def is_presented(self) -> bool:
        return self.entry_element.is_presented()

    def size(self) -> int:
        return self.entry_element.get_count()

    def get_column_value(self, column_name) -> str:
        try:
            index = self.get_header_cell_by_name(column_name)
        except KeyError:
            raise ValueError(f'Column {column_name} does not exist')
        try:
            return self.get_body_cell_value_by_index(index)
        except IndexError:
            raise ValueError(f'Rows have changed or the column index {index} is invalid for {column_name}')

    def get_column_values(self, column_name):
        try:
            index = self.get_header_cell_by_name(column_name)
        except KeyError:
            raise ValueError(f'Column {column_name} does not exist')

        column_values = []
        try:
            body_rows = self.parent_table_ini.body_row.get_page_elements()
            for row in body_rows:
                cell_value = row.join_(FindBy.locator('td')).or_(row.join_(FindBy.locator('th'))) \
                    .of_index_(index).get_text()
                column_values.append(cell_value)
        except IndexError:
            raise ValueError(f'Rows have changed or the column index {index} is invalid for {column_name}')

        return column_values
