import uuid
from typing import Dict
from dataclasses import dataclass, field
from src.models.model import Model
from src.models.reports.report import Report
from src.common.mailgun import Mailgun, MailgunException

USStateDict = {}


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(default="alerts", init=False)
    report_id: str
    case_limit: int
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.report = Report.get_by_id(self.report_id)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "case_limit": self.case_limit,
            "user_email": self.user_email,
            "report_id": self.report_id
        }

    def load_report_details(self):
        self.report.load_data()
        new_case = self.report.current['positiveIncrease']
        return new_case

    def notify_if_limit_reached(self) -> None:
        if self.report.current['positiveIncrease'] > self.case_limit:
            print(f"{self.report.state_name} has more than {self.case_limit} new cases today, number of new cases: {self.report.current['positiveIncrease']}")
            try:
                Mailgun.send_email(
                    [self.user_email],
                    f"Covid-19 Alert for {self.report.state_name}",
                    f"New cases in {self.report.state_name} has reached over {self.case_limit}. New cases updated today is {self.report.current['positiveIncrease']}.\nSummary:\nNew cases:{self.report.current['positiveIncrease']}\nTotal cases: {self.report.current['positive']}\nTotal tests: {self.report.current['posNeg']}\nTotal deaths: {self.report.current['death']}\nTotal hospitalized: {self.report.current['hospitalized']}\nCurrently hospitalized: {self.report.current['hospitalizedCurrently']}",
                    '<p> Please click the following link to log in and view your subscriptions.</p><p>Click <a href="https://covid19-alert.herokuapp.com">here</a> to continue.</p>'
                )
                print(f"Alert sent to {self.user_email} for {self.report.state_name}.")
            except MailgunException:
                print(f"You can't receive email through {email} from mailgun. Please contact the administrator.")
