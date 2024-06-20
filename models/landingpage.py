from selene import browser, command
from selene.support.conditions import have

class LandingPageMethods:

    def __init__(self):
        self.open_offers = browser.element('[class="nav-link"][href="/offers/"]')
        self.open_services = browser.element('[class="nav-link"][href="/services/"]')
        self.offers = browser.element('#id_search')
        self.results = browser.element('.white-bg')
        self.title = browser.element('[class="title"]')

    def open_offers_tab(self):
        self.open_offers.click()

    def open_services_tab(self):
        self.open_services.click()

    def find_offers(self, value):
        self.offers.send_keys(value).press_enter()

    def checking_results(self, value):
        assert self.results.perform(command.js.scroll_into_view).should(have.text(value))
        
    def checking_title(self, value):
        self.title.should(have.text(value))



