from src.models.alerts.alert import Alert
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()


def send_alerts():
    load_dotenv()
    alerts = Alert.all()

    for alert in alerts:
        alert.load_report_details()
        alert.notify_if_limit_reached()
        alert.json()


@sched.scheduled_job('cron', hour=23)
def scheduled_job():
    send_alerts()


sched.start()
