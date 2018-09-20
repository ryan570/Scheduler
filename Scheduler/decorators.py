from flask_login import current_user
from flask import flash, redirect, url_for, session
from Scheduler.model import db, User
from functools import wraps

def admin_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.is_admin():
            return func(*args, **kwargs)
        else:
            flash('Error accessing page', 'danger')
            return redirect(url_for("regular.home"))
    return wrap

def tutor_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.is_tutor():
            return func(*args, **kwargs)
        else:
            flash('Error accessing page', 'danger')
            return redirect(url_for("regular.home"))
    return wrap