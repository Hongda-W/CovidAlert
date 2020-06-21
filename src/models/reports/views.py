import io
import base64
from flask import Blueprint, render_template, redirect, url_for, flash
from src.models.alerts.alert import Alert
from src.models.reports.report import Report
from src.models.users import requires_login, requires_admin
from src.common.state import code_name

report_blueprint = Blueprint('reports', __name__)

state_names = [ele["name"] for ele in code_name]


@report_blueprint.route("/")
@requires_login  # In Flask this decorator must go under the route decorator
def index():
    reports = Report.all()
    subscribers = []
    for report in reports:
        report.load_data()
        alerts = Alert.find_many_by("report_id", report._id)
        subscribers.append(len(alerts))
    sind = sorted(range(len(subscribers)), key=lambda k: -subscribers[k])
    reports = [reports[i] for i in sind]
    subscribers = [subscribers[i] for i in sind]
    for report in reports:
        report.load_data()
    return render_template('reports_index.html', reports=reports, subscribers=subscribers)


@report_blueprint.route("/delete/<string:report_id>")
@requires_admin
def delete_report(report_id):
    report = Report.get_by_id(report_id)
    try:
        alerts = Alert.find_many_by("report_id", report_id)
        for alert in alerts:
            alert.remove_from_mongo()
            flash(f"Alert for {alert.report.state_name} with threshold of {alert.case_limit} cases removed.", "danger")
    except TypeError:
        print(f"No alerts associated with {report.state_name}.")
    report.remove_from_mongo()
    flash(f"Report for {report.state_name} removed from database.", "danger")
    return redirect(url_for('.index'))


@report_blueprint.route('/plot/<string:report_id>', methods=["GET"])
@requires_login
def plot_report(report_id):
    report = Report.get_by_id(report_id)
    fig = report.plot_historic()
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    fig_url = base64.b64encode(img.getvalue()).decode()

    return render_template('image.html', image=fig_url, report=report)
