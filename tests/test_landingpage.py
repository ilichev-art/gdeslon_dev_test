from selene import browser
import allure
from models.landing_page import LandingPageMethods



landing = LandingPageMethods()


def test_search_offer(setup_browser):

    with allure.step('Open offers tab'):
        browser.open('/offers')

    with allure.step('Find offers'):
        landing.find_offers('aliexpress')

    with allure.step('Check results'):
        landing.checking_results('AliExpress RU&CIS')