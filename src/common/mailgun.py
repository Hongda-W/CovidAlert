import os
from typing import List
from requests import Response, post
from dotenv import load_dotenv
load_dotenv()


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun:
    FROM_TITLE = os.environ.get("FROM_TITLE")
    FROM_EMAIL = os.environ.get("FROM_EMAIL")

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str) -> Response:
        api_key = os.environ.get("MAILGUN_API_KEY", None)
        domain = os.environ.get("MAILGUN_DOMAIN", None)
        if api_key is None:
            raise MailgunException('Failed to load Mailgun API key.')
        if domain is None:
            raise MailgunException('Failed to load Mailgun domain.')
        response = post(f"{domain}/messages",
                        auth=("api", api_key),
                        data={
                            "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                            "to": email,
                            "subject": subject,
                            "text": text
                        })
        if response.status_code != 200:
            print(response.json())
            raise MailgunException('An error occurred while sending e-mail.')
        return response
