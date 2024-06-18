import os
from allure_commons.types import Severity
from selene import browser
import allure
from models.homepage import LoginPageMethods


auth = LoginPageMethods()
@allure.title('Авторизация')
@allure.tag('web')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Artem')
@allure.feature(f'Авторизация пользователя на сайте')


def test_login_on_site():
    login = os.getenv("GDESLON_LOGIN")
    password = os.getenv("GDESLON_PASSWORD")


    with allure.step("Open site"):
        browser.open('/')

    with allure.step('Login'):
        auth.login_button()
        auth.fill_user_login(login)
        auth.fill_user_password(password)

    with allure.step('Click enter'):
        auth.click_enter_button()

    with allure.step('Cheking login'):
        auth.check_authorization()





