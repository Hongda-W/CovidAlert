import os
from src.models.alerts.alert import Alert
from src.models.users.user import User
from dotenv import load_dotenv


load_dotenv()
alerts = Alert.all()

# print(os.environ.get("FROM_TITLE"))
# print(os.environ.get("FROM_EMAIL"))
# print(os.environ.get("MAILGUN_API_KEY", None))
# print(os.environ.get("MAILGUN_DOMAIN", None))
# print(os.environ.get('ADMIN'))
# print(os.environ.get('DEBUG'))
User.welcome("example@example.com")

# for alert in alerts:
#     alert.load_report_details()
#     alert.notify_if_limit_reached()
#     alert.json()
#
# if not alerts:
#     print("No alerts have been created. Add an item and an alert to begin!")
