import os
from selene import browser
import allure
from models.home_page import LoginMethods
from dotenv import load_dotenv

auth = LoginMethods()




def test_login_on_site():
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
