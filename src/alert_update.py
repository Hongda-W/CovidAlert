from src.models.alerts.alert import Alert
from dotenv import load_dotenv


load_dotenv()
alerts = Alert.all()

for alert in alerts:
    alert.load_report_details()
    alert.notify_if_limit_reached()
    alert.json()

if not alerts:
    print("No alerts have been created. Add an item and an alert to begin!")