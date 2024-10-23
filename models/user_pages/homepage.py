from selene import browser, command
from selene.support.conditions import be


class LoginPage:

    def __init__(self):
        self.login = browser.element('#login')
        self.fill_login = browser.element('#id_username')
        self.fill_password = browser.element('#id_password')
        self.click_enter = browser.element('.btn')

    def login_button(self):
        self.login.click()

    def fill_user_login(self, value):
        self.fill_login.type(value)

    def fill_user_password(self, value):
        self.fill_password.type(value)

    def click_enter_button(self):
        self.click_enter.perform(command.js.scroll_into_view).click()

    def check_authorization(self):
        assert browser.element('.short').should(be.visible)
