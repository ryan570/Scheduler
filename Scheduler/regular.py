from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint, request, jsonify
from sqlalchemy.sql import func
from Scheduler.forms import RegisterForm, SigninForm, AnnouncementForm
from Scheduler.model import db, User, Announcement
from Scheduler.user import create_user
from Scheduler.announcement import create_announcement
from Scheduler.decorators import admin_required
from Scheduler.calendargenerator import createCalendar, monthString, customMonth
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime
import bcrypt
import json
import os

regular = Blueprint('regular', __name__, template_folder='templates')

@regular.route('/')
def home():
    return render_template('home.html')

@regular.route('/calendar')
def calendar():
    calendar = createCalendar()
    month = monthString(datetime.now().month)
    return render_template('calendar.html', calendar=calendar, month=month, year=datetime.now().year, next=str(datetime.now().month + 1), prev=str(datetime.now().month - 1))

@regular.route('/month/<month>/')
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

@regular.route('/about')
def about():
    return render_template('about.html')

@regular.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
  
    if form.validate_on_submit():
        check1 = form.password.data
        check2 = form.confirmpassword.data
        if check1 == check2:
            if User.query.filter_by(email=form.email.data).first():
                flash('That email is already linked to an account', 'danger')
                return redirect(url_for('regular.register'))
            else:
                user = create_user(form.firstname.data, form.lastname.data, form.grade.data, form.email.data, form.password.data)
                login_user(user,remember=True)
                session['logged_in'] = True
                session['username'] = form.firstname.data + " " + form.lastname.data
                return render_template('home.html')
        else:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('regular.register'))
    else:
        return render_template('register.html', form=form)

@regular.route('/login', methods=['GET', 'POST'])
def login():
    form = SigninForm(request.form)
  
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user,remember=True)
            flash('You have been logged in', 'success')
            session['logged_in'] = True
            session['username'] = user.firstname + ' ' + user.lastname
            if user.is_admin():
                session['admin'] = True
            return redirect(url_for('regular.home'))
        else:
            flash('Invalid Email or Password', 'danger')
            return render_template('login.html', form=form)
                 
    else:
        return render_template('login.html', form=form)


@regular.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('regular.home'))

@regular.route('/dashboard')
@admin_required
def dashboard():
    announcements = Announcement.query.all()
    list.reverse(announcements)
    if len(announcements) > 0:
        return render_template('dashboard.html', announcements=announcements)
    else:
        msg = 'No Announcements Found'
        return render_template('dashboard.html', msg=msg)