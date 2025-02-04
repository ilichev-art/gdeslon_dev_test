import threading

import requests
from aqa_ui.selen.web_browser.web_browser import WebBrowser
from aqa_utils.log_util import log

from config.credentials import UserCredentials
from config.settings import ADMIN_URL, ROOT_URL

# SMART_ID_URL = 'https://dev-smartid.zonesmart.ru/api'
# IDENTITY_URL = f'{SMART_ID_URL}/user/identify/'
# VERIFICATION_URL = f'{SMART_ID_URL}/user/send_verification_email/'
# VERIFY_CODE_URL = f'{SMART_ID_URL}/user/verify_email_code/'
# AUTH_URL = f'{SMART_ID_URL}/user/standard_auth/'
# KID_TOKEN_URL = f'{SMART_ID_URL}/partner/get_user_token_for_site/'
# SESSION_URL = f'{ROOT_URL}/api/auth/admin/kid/'
# SITE_ID = '0b37ff18-8341-49d9-ae07-6dd9fa6c6bb5'


class SessionController:
    __thread = threading.local()

    @classmethod
    def __init_session(cls, creds: 'UserCredentials', timeout: int) -> bool:
        """
        Initialize an API session for the given user credentials.
        If the credentials match the existing thread-local session, reuse it and return False
        Otherwise, reset and create a new session and return True
        """
        if not hasattr(cls.__thread, 'creds') or cls.__thread.creds.email != creds.email:
            if hasattr(cls.__thread, 'creds'):
                log.debug(f'Resetting session for {cls.__thread.creds.email} ...')
            cls.__reset_thread()
            WebBrowser.with_timeout(timeout)
            cls.__create_new_session(creds)
            return True
        else:
            log.debug(f'Reusing existing session for {creds.email}')
            return False

    @classmethod
    def __create_new_session(cls, creds: 'UserCredentials'):
        """
        Initialize an API session for the given user credentials.
        """
        log.debug(f'Creating API session for user {creds.email} ...')
        cls.__thread.creds = creds
        cls.__thread.session = requests.Session()

        try:
            cls.__thread.user_id = cls.__get_user_id()
            cls.__thread.verification_code = cls.__send_verification_code()
            cls.__verify_code()
            cls.__thread.access_token = cls.__authenticate_user()
            cls.__thread.kid_token = cls.__get_kid_token()
            cls.__set_session()
            log.debug('API session created successfully')
        except Exception as e:
            log.error(f'Error during session initialization: {e}')
            raise

    @classmethod
    def __reset_thread(cls):
        """
        Clear all thread-local data to safely reset the session.
        """
        cls.__thread.creds = None
        cls.__thread.session = None
        cls.__thread.user_id = None
        cls.__thread.verification_code = None
        cls.__thread.access_token = None
        cls.__thread.kid_token = None

    @classmethod
    def __get_user_id(cls) -> str:
        response = cls.__thread.session.post(IDENTITY_URL, json={'phone': cls.__thread.creds.phone})
        return cls.__parse_response(response, key='user.id')

    @classmethod
    def __send_verification_code(cls) -> str:
        response = cls.__thread.session.post(
            VERIFICATION_URL,
            json={'action': 'SIGNIN', 'user': cls.__thread.user_id, 'email': cls.__thread.creds.phone}
        )
        return cls.__parse_response(response, key='email_verification')

    @classmethod
    def __verify_code(cls):
        response = cls.__thread.session.post(
            VERIFY_CODE_URL, json={'code': '9999', 'email_verification': cls.__thread.verification_code}
        )
        response.raise_for_status()

    @classmethod
    def __authenticate_user(cls) -> str:
        response = cls.__thread.session.post(
            AUTH_URL,
            json={'user': cls.__thread.user_id,
                  'email_verification': cls.__thread.verification_code,
                  'phone_verification': ''}
        )
        return cls.__parse_response(response, key='jwt.access')

    @classmethod
    def __get_kid_token(cls) -> str:
        response = cls.__thread.session.post(
            KID_TOKEN_URL,
            json={'site': SITE_ID},
            headers={'Authorization': f'JWT {cls.__thread.access_token}'}
        )
        return cls.__parse_response(response, key='token')

    @classmethod
    def __set_session(cls):
        response = cls.__thread.session.get(f'{SESSION_URL}?token={cls.__thread.kid_token}')
        response.raise_for_status()

    @classmethod
    def __parse_response(cls, response: requests.Response, key: str) -> str | None:
        try:
            response.raise_for_status()
            data = response.json()
            value = cls.__get_nested_value(data, key)
            if value is None:
                log.error(f"Key '{key}' not found in response: {data}")
            return value
        except (ValueError, requests.RequestException) as e:
            log.error(f'Failed to parse response: {e}')
            raise

    @staticmethod
    def __get_nested_value(data: dict, key: str) -> str | None:
        """
        Get nested value from a dictionary using a dot-separated key path.
        """
        keys = key.split('.')
        for k in keys:
            if isinstance(data, dict):
                data = data.get(k)
            else:
                return None
        return data

    @classmethod
    def session(cls) -> requests.Session:
        return cls.__thread.session

    @classmethod
    def user_email(cls) -> str:
        return cls.__thread.creds.email

    @classmethod
    def create_user_session(cls, request, creds: UserCredentials):
        log.debug(f'Creating user browser session for user {creds.email} ...')
        worker_id = request.config.workerinput['workerid']
        timeouts = {
            'gw1': 5,
            'gw2': 10,
            'gw3': 15
        }
        timeout = timeouts.get(worker_id, 0)
        new_session = cls.__init_session(creds=creds, timeout=timeout)
        if new_session:
            try:
                WebBrowser.navigate(ROOT_URL) \
                    .add_cookie({'name': 'sessionid', 'value': cls.__thread.session.cookies['sessionid']}) \
                    .add_cookie({'name': 'csrftoken', 'value': cls.__thread.session.cookies['csrftoken']}) \
                    .navigate(ADMIN_URL)
                log.debug('User browser session created: OK')
            except Exception as e:
                log.error(f'Error creating browser session: {e}')
                raise

    @classmethod
    def remove_user_session(cls):
        log.debug(f'Removing user session from the browser {cls.__thread.creds.email} ...')
        try:
            WebBrowser.delete_all_cookies().refresh()
            log.debug('User sessions removed from the browser: OK')
        except Exception as e:
            log.error(f'Error removing user sessions from the browser: {e}')
            raise
