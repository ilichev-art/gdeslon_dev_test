import base64
import os
import pickle
from datetime import datetime
from typing import Dict, Optional, Any
import re

import pytz
from bs4 import BeautifulSoup

from aqa_ui.selen.utils.waiter import Wait
from aqa_utils.log_util import log
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

gmail_client_instances = {}


class GmailClient:
    SCOPES = ['https://mail.google.com/']
    MAX_RESULTS = 100
    INBOX_LABEL = 'INBOX'

    def __init__(self, user_email: str, cred_token_path: str):
        self.user_email = user_email
        self.cred_token_path = cred_token_path
        self.gmail = self._create_gmail_service()

    def _create_gmail_service(self):
        creds = None
        token_path = os.path.join(self.cred_token_path, f'token_{self.user_email}.json')

        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(os.path.join(self.cred_token_path, 'credentials.json'),
                                                                 self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def get_message_id(self, query=''):
        try:
            response = self.gmail.users().messages().list(userId=self.user_email,
                                                          labelIds=[self.INBOX_LABEL],
                                                          q=query,
                                                          maxResults=self.MAX_RESULTS).execute()
            messages = response.get('messages', [])
            if messages:
                return messages[0]['id']
            else:
                raise AssertionError(f'No messages found with query: {query}')
        except HttpError as e:
            raise Exception(f'An error occurred: {e}')

    def get_message_by_id(self, message_id):
        try:
            message = self.gmail.users().messages().get(userId=self.user_email, id=message_id).execute()
            return GmailMessage(message)
        except HttpError as e:
            raise Exception(f'An error occurred: {e}')

    def get_message_by_query(self, message_query):
        try:
            msg_id = self.get_message_id(message_query)
            return self.get_message_by_id(msg_id)
        except HttpError as e:
            raise Exception(f'An error occurred: {e}')

    def get_latest_message_id(self, query=''):
        return self.get_message_id(query)

    def wait_for_latest_email_to_change(self, latest_email_id, max_wait_seconds=300):
        log.debug('Waiting to receive new email message...')
        Wait.until(
            lambda d: self.get_latest_message_id() != latest_email_id,
            timeout=max_wait_seconds,
            log_on_fail=f'Email was not received after waiting for {max_wait_seconds} seconds'
        )
        log.debug('New Email received')
        return self.get_last_email()

    def get_last_email(self):
        latest_email_id = self.get_latest_message_id()
        return self.get_message_by_id(latest_email_id)

    def mark_as_read(self, message_id):
        try:
            modify_request = {'removeLabelIds': ['UNREAD']}
            self.gmail.users().messages().modify(userId=self.user_email, id=message_id, body=modify_request).execute()
        except HttpError as e:
            raise Exception(f'An error occurred: {e}')

    def delete_latest_email(self, total_count_to_delete=1, query: Optional[str] = None):
        try:
            if query:
                message_id = self.get_message_id(query)
                self.gmail.users().messages().delete(userId=self.user_email, id=message_id).execute()
            else:
                for _ in range(total_count_to_delete):
                    latest_email_id = self.get_latest_message_id()
                    self.gmail.users().messages().delete(userId=self.user_email, id=latest_email_id).execute()
        except HttpError as e:
            raise Exception(f'An error occurred: {e}')

    def get_gmail_labels(self) -> Dict[str, str]:
        try:
            response = self.gmail.users().labels().list(userId=self.user_email).execute()
            labels = response.get('labels', [])
            labels_map = {label['id']: label['name'] for label in labels}
            if not labels_map:
                raise Exception('No labels found.')
            return labels_map
        except HttpError as e:
            raise Exception(f'An error occurred: {e}')

    def clean_up_sent_mails(self, obj=None, count=1):
        if obj:
            self.delete_latest_email(count)

    def get_user_mail(self):
        return self.user_email

    def get_activation_link(self):
        latest_msg_id = self.get_latest_message_id()
        self.wait_for_latest_email_to_change(latest_msg_id)

        msg = self.get_message_by_query('Чтобы завершить регистрацию, пройдите по ссылке:')
        soup = BeautifulSoup(msg.get_content(True, 'UTF-8'), 'html.parser')
        activation_link = soup.find('a', href=lambda href: href and 'accounts/registration/activate' in href)

        if msg:
            self.delete_latest_email()

        if activation_link:
            return activation_link['href']

    def is_message_delivered(self, message_query, delete_after=True):
        latest_msg_id = self.get_latest_message_id()
        self.wait_for_latest_email_to_change(latest_msg_id)

        try:
            msg = self.get_message_by_query(message_query)
            return True if msg else False
        except AssertionError:
            log.error(f'Actual message preview: {self.get_last_email().get_preview()}')
            return False
        finally:
            if delete_after:
                log.debug(f'Delete email message: {message_query}')
                self.delete_latest_email()


def get_gmail_instance(user_email, cred_token_path) -> GmailClient:
    if user_email not in gmail_client_instances:
        gmail_client_instances[user_email] = GmailClient(user_email, cred_token_path)
    return gmail_client_instances[user_email]


class GmailMessage:
    def __init__(self, message: Dict[str, Any]):
        self.message = message

    def get_content(self, html_format=False, charset='UTF-8') -> str:
        content = ""
        format_type = "text/html" if html_format else "text/plain"
        payload = self.message.get('payload')

        if payload is None:
            raise ValueError("Gmail message payload is null!")

        body_data = payload.get('body', {}).get('data')
        parts = payload.get('parts')

        if body_data:
            content = base64.urlsafe_b64decode(body_data).decode(charset)
        elif parts:
            content = self._get_alternative_content(payload, html_format, format_type)
            for part in parts:
                if part.get('mimeType') == format_type:
                    part_data = part.get('body', {}).get('data')
                    if part_data:
                        content += base64.urlsafe_b64decode(part_data).decode(charset)
        else:
            raise ValueError("Gmail message payload body is null!")

        return content

    @staticmethod
    def _get_alternative_content(payload: Dict[str, Any], html_format: bool, format_type: str) -> str:
        if html_format:
            is_alternative = any(part.get('mimeType') != format_type for part in payload.get('parts', []))
            if is_alternative:
                for part in payload.get('parts', []):
                    if part.get('mimeType') == "multipart/alternative":
                        for subpart in part.get('parts', []):
                            if subpart.get('mimeType') == format_type:
                                part_data = subpart.get('body', {}).get('data')
                                if part_data:
                                    return base64.urlsafe_b64decode(part_data).decode('UTF-8')
        return ""

    def get_html_format_content(self) -> str:
        return self.get_content(True, 'Windows-1252')

    def get_size(self) -> int:
        return self.message.get('sizeEstimate')

    def get_preview(self) -> str:
        return self.message.get('snippet')

    def get_date(self, pattern: str = '%Y-%m-%d %H:%M:%S') -> str:
        timestamp = int(self.message.get('internalDate')) / 1000
        return datetime.fromtimestamp(timestamp, pytz.UTC).strftime(pattern)

    def get_id(self) -> str:
        return self.message.get('id')

    def get_header(self, header_name: str) -> Optional[str]:
        headers = self.message.get('payload', {}).get('headers', [])
        for header in headers:
            if header.get('name') == header_name:
                return header.get('value')
        return None

    def get_headers(self) -> Dict[str, str]:
        headers = self.message.get('payload', {}).get('headers', [])
        headers_dict = {header.get('name'): header.get('value') for header in headers}
        return headers_dict

    def get_subject(self) -> str:
        return self.get_header('Subject')

    def get_sender(self) -> str:
        return self.get_header('From')

    def get_reply_to(self) -> str:
        return self.get_header('Reply-To')

    def get_recipient(self) -> str:
        return self.get_header('To')

    def get_anchor_redirect_url(self, link_text: str) -> str:
        soup = BeautifulSoup(self.get_content(True, 'UTF-8'), 'html.parser')
        anchor = soup.find('a', string=link_text)
        if anchor:
            return anchor.get('href', '')
        return ''

    def get_registration_link(self, link_title: str) -> str:
        soup = BeautifulSoup(self.get_html_format_content(), 'html.parser')
        anchor = soup.find('a', string=link_title)
        if anchor:
            return anchor.get('href', '')
        raise ValueError(f'Registration URL was not found: {link_title}')

    def get_redirect_url_by_match(self, matcher: str) -> str:
        match = re.search(matcher, self.get_html_format_content())
        if match:
            return match.group().replace('&amp;', '&')
        return ''
