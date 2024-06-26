from allure_commons.types import Severity
import allure
from models.landingpage import LandingPageMethods


landing = LandingPageMethods()

@allure.title('Поиск оффера')
@allure.tag('web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Artem')
@allure.feature(f'Работа поисковой строки в разделе Офферы')


def test_search_offer(setup_browser):

    with allure.step('Open site'):
        landing.open_landingpage()

    with allure.step('Open offers tab'):
        landing.open_offers_tab()

    with allure.step('Find offers'):
        landing.find_offers('aliexpress')

    with allure.step('Check results'):
        landing.checking_results('AliExpress')


@allure.title('Раздел Услуги')
@allure.tag('web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Artem')
@allure.feature(f'Работа отображения текста в разделе Услуги')

def test_services_title(setup_browser):

    with allure.step('Open site'):
        landing.open_landingpage()

    with allure.step('Open services tab'):
        landing.open_services_tab()

    with allure.step('Cheking title'):
        landing.checking_title('Услуги')
