import datetime
import requests
import json
import uuid
from matplotlib.pyplot import subplots
from matplotlib.dates import ConciseDateFormatter, AutoDateLocator
from typing import Dict, List
from dataclasses import dataclass, field
from src.models.model import Model
from src.common.state import State
import matplotlib
matplotlib.pyplot.switch_backend('Agg')


@dataclass(eq=False)  # cannot compare two alert instances
class Report(Model):
    collection: str = field(init=False, default="reports")
    state_code: str
    state_name: str = field(default=None)
    state_info: Dict = field(default=None)
    current: Dict = field(default=None)
    historic: List[Dict] = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.state_code = self.state_code.upper()
        state = State(self.state_code)
        self.state_name = state.name
        self.state_info = state.info

    def load_current(self) -> Dict:
        if self.state_code.lower() == "all":
            url = "https://covidtracking.com/api/v1/us/current.json"
            response = requests.get(url)
            current = json.loads(response.content)[0]
        else:
            url = f"https://covidtracking.com/api/v1/states/{self.state_code.lower()}/current.json"
            response = requests.get(url)
            current = json.loads(response.content)
        return current

    def load_historic(self) -> List[Dict]:
        if self.state_code.lower() == "all":
            url = "https://covidtracking.com/api/v1/us/daily.json"
        else:
            url = f"https://covidtracking.com/api/v1/states/{self.state_code.lower()}/daily.json"
        response = requests.get(url)
        historic = json.loads(response.content)
        return historic

    def load_data(self):
        current = self.load_current()
        self.current = {
            'date': datetime.datetime.strptime(str(current['date']), "%Y%m%d"),
            'positive': current['positive'],
            'negative': current['negative'],
            'posNeg': current['posNeg'],
            'death': current['death'],
            'hospitalized': current['hospitalized'],
            'hospitalizedCurrently': current['hospitalizedCurrently'],
            'recovered': current['recovered'],
            'positiveIncrease': current['positiveIncrease']
        }
        self.current['dateString'] = self.current['date'].strftime("%Y-%m-%d")
        historic = self.load_historic()
        self.historic = []
        for hist in historic:
            self.historic.append({
                'date': datetime.datetime.strptime(str(hist['date']), "%Y%m%d"),
                'positive': hist['positive'],
                'negative': hist['negative'],
                'posNeg': hist['posNeg'],
                'death': hist['death'],
                'hospitalized': hist['hospitalized'],
                'hospitalizedCurrently': hist['hospitalizedCurrently'],
                'recovered': hist['recovered']
            })

    def plot_historic(self):
        dates = []
        positives = []
        hospitalizeds = []
        death_rates = []
        pos_rates = []
        for hist in self.historic:
            date = hist['date']
            positive = hist['positive']
            hospitalized = hist['hospitalized']
            posneg = hist['posNeg']
            death = hist['death']
            dates.append(date)
            if positive:
                positives.append(positive)
                if posneg:
                    pos_rates.append(positive/posneg*100)
                else:
                    pos_rates.append(float("nan"))
            else:
                positives.append(float("nan"))
                pos_rates.append(float("nan"))

            if death and posneg:
                death_rates.append(death/positive*100)
            else:
                death_rates.append(float("nan"))

            if hospitalized:
                hospitalizeds.append(hospitalized)
            else:
                hospitalizeds.append(float("nan"))

        fig, axs = subplots(2, 1, sharex=True, figsize=(10, 7))

        title_fs = 24
        label_fs = 18
        tick_fs = 12
        axs[1].set_xlabel("Date", fontsize=label_fs)

        ax1 = axs[0].twinx()
        axs[0].set_ylabel("Positive cases", fontsize=label_fs, color='r')
        ax1.set_ylabel("Hospitalized cases", fontsize=label_fs, color='b')
        axs[0].plot(dates, positives, 'r', lw=5)
        ax1.plot(dates, hospitalizeds, 'b', lw=5)
        axs[0].tick_params(axis='y', labelcolor='r', labelsize=tick_fs)
        ax1.tick_params(axis='y', labelcolor='b', labelsize=tick_fs)
        axs[0].ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))
        ax1.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

        ax2 = axs[1].twinx()
        axs[1].set_ylabel("Positive rate (%)", fontsize=label_fs, color='r')
        ax2.set_ylabel("Death rate (%)", fontsize=label_fs, color='b')
        axs[1].plot(dates, pos_rates, 'r', lw=5)
        ax2.plot(dates, death_rates, 'b', lw=5)
        axs[1].tick_params(axis='y', labelcolor='r', labelsize=tick_fs)
        ax2.tick_params(axis='y', labelcolor='b', labelsize=tick_fs)

        locator = AutoDateLocator()
        formatter = ConciseDateFormatter(locator)
        axs[1].xaxis.set_major_formatter(formatter)
        axs[1].xaxis.set_major_locator(locator)
        axs[1].tick_params(axis='x', labelsize=label_fs)

        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.suptitle(self.state_name, fontsize=title_fs)
        # fig.savefig('test.png')
        return fig

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "state_code": self.state_code,
            "state_name": self.state_name,
            "state_info": self.state_info,
            "current": self.current,
            "historic": self.historic,
        }
