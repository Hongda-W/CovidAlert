from flask import Flask, render_template
from src.common.database import Database
from src.models.users.views import user_blueprint
from src.models.alerts.views import alert_blueprint


app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialize()


app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")


@app.route('/')
def home():
    return render_template('home.html')