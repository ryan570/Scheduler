from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint, request, jsonify
from sqlalchemy.sql import func
from Scheduler.forms import RegisterForm, SigninForm, AnnouncementForm, EventForm
from Scheduler.model import db, User, Announcement, TutoringSession
from Scheduler.user import create_user
from Scheduler.announcement import create_announcement
from Scheduler.decorators import admin_required, tutor_required
from Scheduler.calendargenerator import createCalendar, monthString, customMonth
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime
import bcrypt
import json
import os

schedule = Blueprint('schedule', __name__, template_folder='templates')

def create_session(date, subject, comments, user, time):
    newSession = TutoringSession(date, subject, comments, user, time)
    db.session.add(newSession)
    db.session.commit()
    return newSession

def delete_session(id):
    tutorSession = TutoringSession.query.filter_by(id=id).first()
    db.session.delete(tutorSession)
    db.session.commit()

def format_time(time):
    if int(time[:2]) > 12:
        h = int(time[:2]) - 12
        ending = ' p.m.'
        formattedTime = str(h) + time[2:] + ending
    else :
        time = time[0:]
        formattedTime = time + ' a.m.'
    return formattedTime

def reverse_time_format(time):
    if len(time) == 9:
        time = '0' + time
    h = time[:2]
    m = time[3:5]    
    if time[6:] == 'p.m.':
        h = int(h) + 12
        return str(h) + ':' + str(m)
    else:
        return str(h) + ':' + str(m)

def format_date(date):
    m = date[5:7]
    d = date[8:10]
    y = date[:4]
    return m + '-' + d + '-' + y

def reverse_date_format(date):
    m = date[:2]
    d = date[3:5]
    y = date[6:]
    return y + '-' + m + '-' + d

def update_sessions(date):
    sessions = TutoringSession.query.all()
    for session in sessions:
        if datetime.strptime(reverse_date_format(session.date) + reverse_time_format(session.time), '%Y-%m-%d%H:%M') < date:
            db.session.delete(session)
    db.session.commit()

def render_calendar(month):
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

def sort_sessions(sessions):
    return sorted(sessions, key=lambda item: item.date)

@schedule.route('/schedulePage')
@login_required
def schedulePage():
    update_sessions(datetime.today())
    if current_user.is_tutor():
        availableSessions = sort_sessions(TutoringSession.query.filter_by(tutor=None).all())
        tutoringSessions = sort_sessions(TutoringSession.query.filter_by(tutor=current_user.get_id()).all())
        return render_template('tutor_schedule.html', availableSessions=availableSessions, tutoringSessions=tutoringSessions)
    else:
        sessions = sort_sessions(TutoringSession.query.filter_by(user=current_user.get_id()).all())
        return render_template('schedule.html', sessions=sessions)

@schedule.route('/add_session', methods=['POST', 'GET'])
@login_required
def addSession():
    form = EventForm(request.form)
    time = str(datetime.now().time())
    if form.validate_on_submit():
        formattedTime = format_time(request.form['timefield'])
        formattedDate = format_date(request.form['datefield'])
        create_session(formattedDate, form.subject.data, form.comments.data, current_user.get_id(), formattedTime)
        flash('Session Requested!', 'success')
        return redirect(url_for('schedule.schedulePage'))
    return render_template('add_session.html', form=form, time=time[:5])

@schedule.route('/accept_session/<id>/', methods=['POST', 'GET'])
@tutor_required
def accept_session(id):
    tutorSession = TutoringSession.query.filter_by(id=id).first()
    tutorSession.tutor = current_user.get_id()
    db.session.commit()
    return redirect(url_for('schedule.schedulePage'))

@schedule.route('/cancel_session/<id>/')
@tutor_required
def cancel_session(id):
    tutorSession = TutoringSession.query.filter_by(id=id).first()
    tutorSession.tutor = None
    db.session.commit()
    return redirect(url_for('schedule.schedulePage'))

@schedule.route('/edit_session/<id>', methods=['POST', 'GET'])
@login_required
def editSession(id):
    tutorSession = TutoringSession.query.filter_by(id=id).first()
    form = EventForm(subject=tutorSession.subject.lower())
    form.comments.data = tutorSession.comments
    date = reverse_date_format(tutorSession.date)
    time = reverse_time_format(tutorSession.time)
    if form.validate_on_submit():
        delete_session(id)
        subject = request.form['subject']
        comment = request.form['comments']
        formattedTime = format_time(request.form['timefield'])
        formattedDate = format_date(request.form['datefield'])
        create_session(formattedDate, subject, comment, current_user.get_id(), formattedTime)
        flash ('Session Edited!', 'success')
        return redirect(url_for('schedule.schedulePage'))
    return render_template('edit_session.html', form=form, date=date, time=time)

@schedule.route('/delete_session/<id>/')
@login_required
def delete(id):
    delete_session(id)
    flash('Tutoring Session Deleted!', 'success')
    return redirect(url_for('schedule.schedulePage'))
    

@schedule.route('/calendar')
@login_required
def calendar():
    if session.get('month') is None:
        calendar = createCalendar()
        month = monthString(datetime.now().month)
        return render_template('calendar.html', calendar=calendar, month=month, year=datetime.now().year, next=str(datetime.now().month + 1), prev=str(datetime.now().month - 1))
    else:
        month = session.get('month')
        session['month'] = None
        return render_calendar(month)

@schedule.route('/month/<month>/')
@login_required
def specificMonth(month):
    session['month'] = month
    return redirect(url_for('schedule.calendar'))