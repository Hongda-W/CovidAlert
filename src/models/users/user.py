import uuid
from dataclasses import dataclass, field
from src.models.model import Model
from typing import Dict
from src.common.utils import Utils
import src.models.users.errors as UserErrors
from src.models.alerts.alert import Alert
from src.common.mailgun import Mailgun


@dataclass
class User(Model):
    collection: str = field(default="users", init=False)
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        try:
            return cls.find_one_by('email', email)
        except TypeError:
            raise UserErrors.UserNotFoundError(f"No user with email {email} was found!")

    @classmethod
    def is_login_valid(cls, email: str, password: str) -> bool:
        user = cls.find_by_email(email)
        if not Utils.check_hashed_password(password, user.password):
            raise UserErrors.IncorrectPasswordError("The password you put in was incorrect!")

        return True

    @classmethod
    def register(cls, email: str, password: str) -> bool:
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError(f"{email} is not a valid email.")
        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError(f"{email} has already been registered.")
        except UserErrors.UserNotFoundError:
            User(email, Utils.hash_password(password)).save_to_mongo()
            cls.welcome(email)

        return True

    @classmethod
    def deregister(cls, email: str) -> bool:
        user = cls.find_by_email(email)
        user.remove_from_mongo()
        alerts = Alert.find_many_by("user_email", email)
        for alert in alerts:
            alert.remove_from_mongo()
        return True

    @classmethod
    def welcome(cls, email: str) -> None:
        Mailgun.send_email(
            [email],
            f"Welcome, you signed up for Covid-19 Alerts",
            f"Thank you for registering your account with us. You can log in and add alerts on our web page. We will "
            f"notify you through email if new cases in your subscribed region exceeds the threshold you "
            f"choose.\n",
            f'<p> Please click the following link to log in and continue exploring.</p><p>Click <a href="https://covid19-alert.herokuapp.com">here</a> to continue.</p>'
        )

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }
