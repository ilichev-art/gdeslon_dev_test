# import requests
# from pprint import pprint
#
# BASE_URL = "https://jsonplaceholder.typicode.com"
#
# # Проверка `GET` запроса
# def test_get_post():
#     response = requests.get(f"{BASE_URL}/posts/1")
#     assert response.status_code == 200
#     data = response.json()
#     pprint(data)
#     assert data["id"] == 1
#     assert "title" in data
#     assert "body" in data
#
# # Проверка `POST` запроса
# def test_create_post():
#     payload = {"title": "foo", "body": "bar", "userId": 1}
#     response = requests.post(f"{BASE_URL}/posts", json=payload)
#     assert response.status_code == 201
#     data = response.json()
#     assert data["title"] == "foo"
#     assert data["body"] == "bar"
#     assert data["userId"] == 1


# def fail_safe(temperature, neutrons_produced_per_second, threshold):
#     """Assess and return status code for the reactor.
#
#     :param temperature: int or float - value of the temperature in kelvin.
#     :param neutrons_produced_per_second: int or float - neutron flux.
#     :param threshold: int or float - threshold for category.
#     :return: str - one of ('LOW', 'NORMAL', 'DANGER').
#
#     1. 'LOW' -> `temperature * neutrons per second` < 90% of `threshold`
#     2. 'NORMAL' -> `temperature * neutrons per second` +/- 10% of `threshold`
#     3. 'DANGER' -> `temperature * neutrons per second` is not in the above-stated ranges
#     """


# def make_word_groups(vocab_words):


# def remove_suffix_ness(word):
#     """Remove the suffix from the word while keeping spelling in mind.
#
#     :param word: str - of word to remove suffix from.
#     :return: str - of word with suffix removed & spelling adjusted.
#
#     For example: "heaviness" becomes "heavy", but "sadness" becomes "sad".
#     """
#     word = word[:-4]
#     if word.endswith('i'):
#         word = word[:-1] + 'y'
#     return word
#
# print(remove_suffix_ness('heaviness'))


# def adjective_to_verb(sentence, index):
#     """Change the adjective within the sentence to a verb.
#
#     :param sentence: str - that uses the word in sentence.
#     :param index: int - index of the word to remove and transform.
#     :return: str - word that changes the extracted adjective to a verb.
#
#     For example, ("It got dark as the sun set.", 2) becomes "darken".
#     """
#     sentence = sentence[:-1]
#     word = sentence.split()[index]
#     verb = word + 'en'
#     return verb
#
# print(adjective_to_verb('I need to make that bright.', -1 ))


# def armstrong(number):
#     numbers = str(number)
#     lenght = len(numbers)
#     result = sum(int(digit) ** lenght for digit in numbers)
#     return result
#
# print(armstrong(10))


# def translate(text):
#     if len(text) == len(set(text)):
#         return True
#     else:
#         return False
#
# print(translate('hello'))

# def is_pangram(sentence):
#     alpha = set("abcdefghijklmnopqrstuvwxyz")
#     sentence = ''.join(chair for chair in sentence if chair.isalpha()).lower()
#     return set(sentence) == alpha
#
# print((is_pangram('Abcdef ghijklmnopqrstuv, xwyz')))


def value_of_card(card):
    """Determine the scoring value of a card.

    :param card: str - given card.
    :return: int - value of a given card.  See below for values.

    1.  'J', 'Q', or 'K' (otherwise known as "face cards") = 10
    2.  'A' (ace card) = 1
    3.  '2' - '10' = numerical value.
    """

    high_cards = ['J', 'Q', 'K', '10']
    if card in high_cards:
        return 10
    elif card == 'A':
        return 1
    else:
        return int(card)


def higher_card(card_one, card_two):
    """Determine which card has a higher value in the hand.

    :param card_one, card_two: str - cards dealt in hand.  See below for values.
    :return: str or tuple - resulting Tuple contains both cards if they are of equal value.

    1.  'J', 'Q', or 'K' (otherwise known as "face cards") = 10
    2.  'A' (ace card) = 1
    3.  '2' - '10' = numerical value.
    """

    if value_of_card(card_one) > value_of_card(card_two):
        return card_one
    elif value_of_card(card_two) > value_of_card(card_one):
        return card_two
    else:
        return card_one, card_two

print(higher_card('4', 'A'))

