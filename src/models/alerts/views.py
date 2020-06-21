import io
import base64
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.models.alerts.alert import Alert
from src.models.reports.report import Report
from src.common.state import State
from src.models.users import requires_login
from src.common.state import code_name

alert_blueprint = Blueprint('alerts', __name__)

state_names = [ele["name"] for ele in code_name]


@alert_blueprint.route("/")
@requires_login  # In Flask this decorator must go under the route decorator
def index():
    alerts = Alert.find_many_by('user_email', session['email'])
    for alert in alerts:
        alert.report.load_data()
    return render_template('alerts_index.html', alerts=alerts)


@alert_blueprint.route("/new", methods=['GET', 'POST'])
@requires_login
def new_alert():
    if request.method == 'POST':
        state_name = request.form.get('state')
        try:
            case_limit = int(request.form['case_limit'])
        except ValueError:
            flash(f"Case threshold must be an integer.", "warning")
            return render_template("new_alert.html", options=state_names)

        try:
            report = Report.find_one_by("state_name", state_name)
        except TypeError:
            state = State(None, state_name)
            report = Report(state.code)
        report.load_data()

        alert = Alert(report._id, case_limit, session['email'])
        alert.save_to_mongo()
        flash(f"Alert for {report.state_name} with {case_limit} cases threshold created successfully.", "success")
        return redirect(url_for('.index'))

    return render_template("new_alert.html", options=state_names)


@alert_blueprint.route("/edit/<string:alert_id>", methods=['GET', 'POST'])
@requires_login
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)

    if request.method == 'POST':
        try:
            case_limit = int(request.form['case_limit'])
        except ValueError:
            flash(f"Case threshold must be an integer.", "warning")
            return render_template('edit_alert.html', alert=alert)

        alert.case_limit = case_limit
        if alert.user_email == session['email']:
            alert.save_to_mongo()
            alert.report.load_data()
            flash(f"Case threshold for {alert.report.state_name} updated to {case_limit}.", "success")
        return redirect(url_for('.index'))

    return render_template('edit_alert.html', alert=alert)


@alert_blueprint.route("/delete/<string:alert_id>")
@requires_login
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session['email']:
        alert.remove_from_mongo()
        flash(f"Alert for {alert.report.state_name} with threshold of {alert.case_limit} cases removed.", "danger")
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