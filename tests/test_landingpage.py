from allure_commons.types import Severity
from selene import browser
import allure
from models.landing_page import LandingPageMethods


landing = LandingPageMethods()

@allure.title('Поиск оффера')
@allure.tag('web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Artem')
@allure.feature(f'Работа поисковой строки в разделе Офферы')


def test_search_offer(setup_browser):

    with allure.step('Open offers tab'):
        browser.open('/offers')

    with allure.step('Find offers'):
        landing.find_offers('aliexpress')

    with allure.step('Check results'):
        landing.checking_results('AliExpress')