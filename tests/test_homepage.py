import os
from allure_commons.types import Severity
import allure
from selene.support.shared import browser

from models.user_pages.homepage import LoginPage

auth_page = LoginPage()


@allure.title('Авторизация пользователя')
@allure.tag('web')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Artem')
@allure.feature(f'Авторизация пользователя на сайте')
@allure.link('https://gdeslon.kokoc.com', name="Link to Home Page")
def test_login_on_site():
    login = os.getenv("GDESLON_LOGIN")
    password = os.getenv("GDESLON_PASSWORD")

    with allure.step("Открыть сайт"):
        browser.open('/')

    with allure.step('Авторизоваться на сайте'):
        auth_page.login_button()
        auth_page.fill_user_login(login)
        auth_page.fill_user_password(password)

    with allure.step('Нажать enter'):
        auth_page.click_enter_button()

    with allure.step('Проверка авторизации'):
        auth_page.check_authorization()
