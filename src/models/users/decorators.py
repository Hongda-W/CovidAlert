import functools
from typing import Callable
from flask import session, flash, redirect, url_for, current_app


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_func(*args, **kwargs):
        if not session.get('email'):
            flash("You need to be signed in for this page.", 'danger')
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated_func


def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_func(*args, **kwargs):
        if not session.get('email'):
            flash('You need to be an administrator to access this function.', 'danger')
            return redirect(url_for('users.login'))
        if session.get('email') != current_app.config.get('ADMIN', ''):
            flash('You need to be an administrator to access this function.', 'danger')
            return redirect(url_for('reports.index'))
        return f(*args, **kwargs)

    return decorated_func
