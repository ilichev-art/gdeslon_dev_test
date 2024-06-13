from selene import browser, by, command
from selene.support.conditions import have, be

class LandingPageMethods:


    def find_offers(self, value):
        browser.element('#id_search').send_keys(value).press_enter()

    def checking_results(self, value):
        assert browser.element('.white-bg').perform(command.js.scroll_into_view).should(have.value(value))