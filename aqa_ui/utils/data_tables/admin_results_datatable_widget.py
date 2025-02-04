from typing import Union

import allure
from aqa_ui.selen.web_page_element.page_element.find_by import FindBy
from aqa_ui.selen.web_page_element.page_element.web_page_element import WebPageElement
from aqa_ui.utils.data_tables.base_data_table_widget import BaseDataTable, BaseDataTableEntry
from aqa_utils.log_util import log


class AdminResultsDataTableWidget(BaseDataTable):
    _table = FindBy.exact_match('table', 'id', 'result_list')

    def __init__(self):
        super().__init__(self._table)

    @allure.step('Identify target entry')
    def get_entry(self, entry):
        log.info(f'Identify target entry: {entry}')
        return AdminDataTableEntry(self, entry)


class AdminDataTableEntry(BaseDataTableEntry):
    def __init__(self, parent_table_ini, entry: Union[int, str] = None):
        super().__init__(parent_table_ini, entry)

    def _checkbox(self) -> WebPageElement:
        return self.entry_element.join_(FindBy.exact_match('input', 'type', 'checkbox'))

    @staticmethod
    def _row_cell_marked_img(yes_or_no) -> WebPageElement:
        return FindBy.partial_match('img', 'src', f'icon-{yes_or_no}')

    @allure.step('Select entry checkbox')
    def select_checkbox(self):
        log.info('Select entry checkbox')
        self._checkbox().click().with_page_load_state()
        return self

    @allure.step('Assert entry checkbox selected')
    def assert_checkbox_selected(self):
        log.info('Assert entry checkbox selected')
        self._checkbox().assert_that().selected()
        return self

    def is_get_row_cell_marked_active(self, cell: str) -> bool:
        log.info(f'Assert row cell is marked as active: {cell}')
        return self.get_column_cell_element(cell).join_(self._row_cell_marked_img('yes')).is_presented()

    def is_get_row_cell_marked_not_active(self, cell: str) -> bool:
        log.info(f'Assert row cell is marked as not active: {cell}')
        return self.get_column_cell_element(cell).join_(self._row_cell_marked_img('no')).is_presented()

    def click_entry_field_id(self):
        self.entry_element.join_(FindBy.class_name('field-id')).locator_('a').click()

    def __get_header_cell_by_class_name(self, entry_class_name: str):
        return self.parent_table_ini.head_cell.get_all_class_names().index(entry_class_name) + 1

    def get_column_cell_element(self, column_cell):
        try:
            index = self.__get_header_cell_by_class_name(column_cell)
        except KeyError:
            raise ValueError(f'Column {column_cell} does not exist')
        try:
            return self.get_body_cell_element_by_index(index)
        except IndexError:
            raise ValueError(f'Rows have changed or the column index {index} is invalid for {column_cell}')

    def get_column_value(self, column_name) -> str:
        try:
            index = self.__get_header_cell_by_class_name(column_name)
        except KeyError:
            raise ValueError(f'Column {column_name} does not exist')
        try:
            return self.get_body_cell_value_by_index(index)
        except IndexError:
            raise ValueError(f'Rows have changed or the column index {index} is invalid for {column_name}')

    def get_column_values(self, column_name):
        try:
            index = self.__get_header_cell_by_class_name(column_name)
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
