import io
import base64
from flask import Blueprint, render_template, request, redirect, url_for, session
from src.models.alerts.alert import Alert
from src.models.reports.report import Report
from src.common.state import State
from src.models.users import requires_login

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route("/")
@requires_login  # In Flask this decorator must go under the route decorator
def index():
    alerts = Alert.find_many_by('user_email', session['email'])
    return render_template('alerts_index.html', alerts=alerts)


@alert_blueprint.route("/new", methods=['GET', 'POST'])
@requires_login
def new_alert():
    if request.method == 'POST':
        state_name = request.form['state']
        case_limit = int(float(request.form['case_limit']))

        try:
            report = Report.find_one_by("state_name", state_name)
            print(report.state_name)
        except TypeError:
            state = State(None, state_name)
            report = Report(state.code)
        report.load_data()
        report.save_to_mongo()

        alert = Alert(report._id, case_limit, session['email'])
        alert.save_to_mongo()
        return redirect(url_for('.index'))

    return render_template("new_alert.html")


@alert_blueprint.route("/edit/<string:alert_id>", methods=['GET', 'POST'])
@requires_login
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)

    if request.method == 'POST':
        case_limit = float(request.form['case_limit'])

        alert.case_limit = case_limit
        if alert.user_email == session['email']:
            alert.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('edit_alert.html', alert=alert)


@alert_blueprint.route("/delete/<string:alert_id>")
@requires_login
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session['email']:
        alert.remove_from_mongo()
    return redirect(url_for('.index'))


@alert_blueprint.route('/plot/<string:alert_id>', methods=["GET"])
@requires_login
def plot_report(alert_id):
    alert = Alert.get_by_id(alert_id)
    report = alert.report
    fig = report.plot_historic()
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    fig_url = base64.b64encode(img.getvalue()).decode()

    return render_template('image.html', image=fig_url, report=report)