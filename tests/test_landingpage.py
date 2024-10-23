from allure_commons.types import Severity
import allure
from selene.support.shared import browser
from models.user_pages.landingpage import LandingPage

landing = LandingPage()


@allure.title('Поиск оффера')
@allure.tag('web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Artem')
@allure.feature(f'Работа поисковой строки в разделе Офферы')
def test_search_offer():
    with allure.step('Открыть сайт'):
        browser.open('/')

    with allure.step('Перейти во вкладку Офферы'):
        landing.open_offers_tab()

    with allure.step('Найти оффер'):
        landing.find_offers('aliexpress')

    with allure.step('Проверить результат'):
        landing.checking_results('AliExpress')


@allure.title('Раздел Услуги')
@allure.tag('web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Artem')
@allure.feature(f'Работа отображения текста в разделе Услуги')
def test_services_title():
    with allure.step('Открыть сайт'):
        browser.open('/')

    with allure.step('Открыть кладку Услуги'):
        landing.open_services_tab()

    with allure.step('Проверить заголовок'):
        landing.checking_title('Услуги')
