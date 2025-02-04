import pytest
import requests


#
#
# def division():
#     num_1 = int(input('введите первое число: '))
#     num_2 = int(input('введите второе число: '))
#     try:
#         return num_1/num_2
#     except :
#         while num_2 <= 0:
#             num_2 = int(input('введите второе число больше 0: '))
#         return num_1/num_2
#
#
# def super_division():
#     division()
#
#
#
#
# super_division()

# @pytest.fixture(params=[10, 20, 30])
# def number(request):
#     return request.param
#
# def test_is_even(number):
#     assert number % 2 == 0
#
#     import pytest
#
# @pytest.fixture()
# def config():
#     return {
#         "base_url": "https://swapi.dev/",
#         "timeout": 5
#     }
#
#
# def test_api_call(config):
#     response = requests.get(config["base_url"], timeout=config["timeout"])
#     assert response.status_code == 200
#
# import pytest
# from selenium import webdriver
#
# @pytest.fixture
# def browser():
#     driver = webdriver.Chrome()
#     yield driver
#     driver.quit()
#
# @pytest.mark.parametrize("url", [
#     "https://www.google.com",
#     "https://www.github.com",
#     "https://www.example.com"
# ])
# def test_open_page(browser, url):
#     browser.get(url)
#     assert browser.title != ""


# def exchangeable_value(budget, exchange_rate, spread, denomination):
#     actual_rate = exchange_rate * (1 + spread / 100)
#     max_value = budget // actual_rate
#     exchangeable = int(max_value // denomination) * denomination
#     return exchangeable
#
# print(exchangeable_value(127.25, 1.20, 10, 5))
#
#
# def eat_ghost(power_pellet_active, touching_ghost):
#     if power_pellet_active and touching_ghost == True:
#         return True
#     else:
#         return False
#
#
# print(eat_ghost(False, True))
#
#
# def score(touching_power_pellet, touching_dot):
#     if touching_power_pellet or touching_dot == True:
#         return True
#     else:
#         return False
#
#
# print(score(True, True))
#
#
# def lose(power_pellet_active, touching_ghost):
#     if power_pellet_active == False and touching_ghost == True:
#         return True
#     else:
#         return False
#
#
# print(lose(False, True))


# def win(has_eaten_all_dots, power_pellet_active, touching_ghost):
#     if power_pellet_active == True and touching_ghost == True and has_eaten_all_dots == True:
#         return True
#     elif power_pellet_active == False and touching_ghost == True and has_eaten_all_dots == True:
#         return False
#     elif power_pellet_active == True and touching_ghost == True and has_eaten_all_dots == False:
#         return False
#     else:
#         return True
#
#
#
# print(win(False, True, True))


# def steps(number):
#     if number <= 0:
#         raise ValueError("Only positive integers are allowed")
#
#     count = 0
#
#     while number != 1:
#
#         if number % 2 == 0:
#             number = number / 2
#         elif number % 2 != 0:
#             number = number * 3 + 1
#         count += 1
#         print(count, int(number))
#
# steps(1)

# print(f'{count + 1}. {int(number)}')

film = {'Titanic': 1997,
        'Avatar': 2005}
new_film = {'Armageddon': 2010}
another_film = {'London': 2020}

merged_films = film | new_film | another_film

print(merged_films)