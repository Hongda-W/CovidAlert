from flask import Blueprint, request, session, url_for, render_template, redirect
from src.models.users import User, UserErrors
from src.models.alerts.alert import Alert
from src.models.users import requires_login

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/')
@requires_login
def index():
    alerts = Alert.find_many_by('user_email', session['email'])
    return render_template('alerts_index.html', alerts=alerts)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register(email, password)
            session['email'] = email
            return redirect(url_for('.index'))
        except UserErrors.UserError as e:
            return e.message

    return render_template('register.html')


@user_blueprint.route('/deregister', methods=['GET', 'POST'])
def deregister():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.is_login_valid(email, password):
                User.deregister(email)
                session['email'] = None
                return render_template('home.html')
        except UserErrors.UserError as e:
            return e.message

    return render_template('deregister.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('.index'))
        except UserErrors.UserError as e:
            return e.message

    return render_template('login.html')


@user_blueprint.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('.login'))
