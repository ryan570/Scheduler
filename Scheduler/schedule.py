from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint, request, jsonify
from sqlalchemy.sql import func
from Scheduler.forms import RegisterForm, SigninForm, AnnouncementForm, EventForm
from Scheduler.model import db, User, Announcement, TutoringSession
from Scheduler.user import create_user
from Scheduler.announcement import create_announcement
from Scheduler.decorators import admin_required
from Scheduler.calendargenerator import createCalendar, monthString, customMonth
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime
import bcrypt
import json
import os

schedule = Blueprint('schedule', __name__, template_folder='templates')

def create_session(date, subject, comments, user):
    newSession = TutoringSession(date, subject, comments, user)
    db.session.add(newSession)
    db.session.commit()
    return newSession

def delete_session(id):
    tutorSession = TutoringSession.query.filter_by(id=id).first()
    db.session.delete(tutorSession)
    db.session.commit()

@schedule.route('/schedulePage')
@login_required
def schedulePage():
    sessions = TutoringSession.query.filter_by(user=current_user.get_id()).all()
    return render_template('schedule.html', sessions=sessions)

@schedule.route('/add_session', methods=['POST', 'GET'])
@login_required
def addSession():
    form = EventForm(request.form)
    if form.validate_on_submit():
        create_session(request.form['datefield'], form.subject.data, form.comments.data, current_user.get_id())
        flash('Session Requested!', 'success')
        return redirect(url_for('schedule.schedulePage'))
    return render_template('add_session.html', form=form)

@schedule.route('/edit_session/<id>', methods=['POST', 'GET'])
@login_required
def editSession(id):
    tutorSession = TutoringSession.query.filter_by(id=id).first()
    form = EventForm(subject=tutorSession.subject.lower())
    form.comments.data = tutorSession.comments
    date = tutorSession.date
    if form.validate_on_submit():
        delete_session(id)
        date = request.form['datefield']
        subject = request.form['subject']
        comment = request.form['comments']
        create_session(date, subject, comment, current_user.get_id())
        flash ('Session Edited!', 'success')
        return redirect(url_for('schedule.schedulePage'))
    flash(form.errors)
    return render_template('edit_session.html', form=form, date=date)

@schedule.route('/delete_session/<id>/')
@login_required
def delete(id):
    delete_session(id)
    flash('Tutoring Session Deleted!', 'success')
    return redirect(url_for('schedule.schedulePage'))
    

@schedule.route('/calendar')
@login_required
def calendar():
    calendar = createCalendar()
    month = monthString(datetime.now().month)
    return render_template('calendar.html', calendar=calendar, month=month, year=datetime.now().year, next=str(datetime.now().month + 1), prev=str(datetime.now().month - 1))

@schedule.route('/month/<month>/')
@login_required
def specificMonth(month):
    year = datetime.now().year
    month = int(month)
    next = month + 1
    prev = month - 1
    while month > 12:
        month -= 12
        year += 1
    while month < 1:
        month += 12
        year -= 1
    calendar = customMonth(month, year)
    monthName = monthString(month)
    return render_template('calendar.html', calendar=calendar, month=monthName, year=year, next=next, prev=prev)