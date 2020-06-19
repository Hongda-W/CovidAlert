from flask import Flask, render_template, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg
from src.common.database import Database
import io
import base64
from src.models.reports.report import Report


app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialize()


# @app.route('/')
# def home():
#     return render_template('home.jinja2')
#
# from src.models.users.views import user_blueprint
# from src.models.stores.views import store_blueprint
# from src.models.alerts.views import alert_blueprint
# app.register_blueprint(user_blueprint, url_prefix="/users")
# app.register_blueprint(store_blueprint, url_prefix="/stores")
# app.register_blueprint(alert_blueprint, url_prefix="/alerts")

# @app.route('/plot', methods=["GET"])
# def plot_show():
#     report = Report('WA')
#     report.load_data()
#     fig = report.plot_historic()
#
#     img = io.BytesIO()
#     FigureCanvasAgg(fig).print_png(img)
#     return Response(img.getvalue(), mimetype='image/png')


@app.route('/plot', methods=["GET"])
def plot_show():
    report = Report('HI')
    report.load_data()
    fig = report.plot_historic()

    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    fig_url = base64.b64encode(img.getvalue()).decode()

    return render_template('image.html', image=fig_url)
