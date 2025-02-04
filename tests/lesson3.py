import requests
from bs4 import BeautifulSoup

WEB_URL = 'https://gdeslon.kokoc.com/'
API_URL = 'https://gdeslon.kokoc.com/accounts/login/'

USER_NAME = 'a.ilichev@dev.kokoc.com'
PASSWORD = '7823659Fuck'
session = requests.Session()

get_resp = session.get(WEB_URL)
soup = BeautifulSoup(get_resp.text, 'html.parser')
csrfmiddlewaretoken = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
csrftoken = session.cookies['csrftoken']

payload = {
    'csrfmiddlewaretoken': csrfmiddlewaretoken,
    'username': USER_NAME,
    'password': PASSWORD
}
headers = {
    'Accept-Language': 'u-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': f'cookielaw_accepted=1; csrftoken={csrftoken}; is_authenticated=0',
}
response = session.post(url=f'{WEB_URL}/accounts/login/',
                        data=payload,
                        headers=headers,
                        allow_redirects=True)

print(response.status_code)

