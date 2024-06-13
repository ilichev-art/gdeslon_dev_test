from selene import browser, by, command
from selene.support.conditions import have, be

class LoginPageMethods:

    def login(self):
        browser.element('#login').click()
    def fill_login(self, value):
        browser.element('#id_username').type(value)
    def fill_password(self, value):
        browser.element('#id_password').type(value).click()
    def click_button(self):
        browser.element('.btn').perform(command.js.scroll_into_view).click()
    def check_authorization(self):
        assert browser.element('.short').should(be.visible)
