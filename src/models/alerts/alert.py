import uuid
from typing import Dict
from dataclasses import dataclass, field
from src.models.model import Model
from src.models.reports.report import Report

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
            print(f"{self.report.state_name} has more than {self.case_limit} new cases today, number of new cases: {self.case_limit}")
