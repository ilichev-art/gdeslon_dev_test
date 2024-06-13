import os

from allure_commons.types import Severity
from selene import browser
import allure
from models.login_page import LoginPageMethods


auth = LoginPageMethods()
@allure.title('Авторизация')
@allure.tag('web')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Artem')
@allure.feature(f'Авторизация пользователя на сайте')


def test_login_on_site(setup_browser):
    login = os.getenv("GDESLON_LOGIN")
    password = os.getenv("GDESLON_PASSWORD")


    with allure.step("Open site"):
        browser.open('/')

    with allure.step('Login'):
        auth.login()
        auth.fill_login(login)
        auth.fill_password(password)

    with allure.step('Click enter'):
        auth.click_button()

    with allure.step('Cheking login'):
        auth.check_authorization()





