from flask import url_for, render_template
from Scheduler.model import db, User
from sqlalchemy import func
from sqlalchemy import and_
import datetime
import calendar
import sys

def create_user(first, last, grade, email, password, tutor):
    newuser = User(first, last, grade, email, password, tutor)
    db.session.add(newuser)
    db.session.commit()
    return newuser