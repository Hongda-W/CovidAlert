import os
from flask import Flask, render_template
from src.common.database import Database
from src.models.users.views import user_blueprint
from src.models.alerts.views import alert_blueprint
from src.models.reports.views import report_blueprint
import jinja2


app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config.update(
    ADMIN=os.environ.get('ADMIN'),
    DEBUG=os.environ.get('DEBUG')
)
app.jinja_env.filters['zip'] = zip


@app.before_first_request
def init_db():
    Database.initialize()


app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(report_blueprint, url_prefix="/reports")


@app.route('/')
def home():
    return render_template('home.html')