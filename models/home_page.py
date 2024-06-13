from selene import browser, by, command
from selene.support.conditions import have, be

class LoginMethods:

    def login(self):
        browser.element('#login').click()
    def fill_login(self, s):
        browser.element('#id_username').type(s)
    def fill_password(self, s):
        browser.element('#id_password').type(s).click()

    def click_button(self):
        browser.element('.btn').perform(command.js.scroll_into_view).click()
    def check_authorization(self):
        assert browser.element('.short').should(be.visible)
