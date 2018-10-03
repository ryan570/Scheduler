from flask import url_for, render_template
from Scheduler.model import db, User
from Scheduler.mail import generate_confirmation_token, send_email
from sqlalchemy import func
from sqlalchemy import and_
import datetime
import calendar
import sys

def create_user(first, last, grade, email, password, tutor):
    newuser = User(first, last, grade, email, password, tutor)
    db.session.add(newuser)
    db.session.commit()
    token = generate_confirmation_token(newuser.email)
    confirm_url = url_for('regular.verify_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(newuser.email, subject, html)
    return newuser