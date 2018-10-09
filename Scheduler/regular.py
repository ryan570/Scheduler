from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint, request, jsonify
from sqlalchemy.sql import func
from Scheduler.forms import RegisterForm, SigninForm, AnnouncementForm, EventForm
from Scheduler.model import db, User, Announcement
from Scheduler.user import create_user
from Scheduler.announcement import create_announcement
from Scheduler.decorators import admin_required
from Scheduler.calendargenerator import createCalendar, monthString, customMonth
from Scheduler.mail import generate_confirmation_token, confirm_token, send_email
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime
import bcrypt
import json
import os

regular = Blueprint('regular', __name__, template_folder='templates')

@regular.route('/', methods=['POST', 'GET'])
def home():
    if not current_user.is_authenticated and session.get('logged_in') == True:
        return redirect(url_for('regular.unconfirmed'))
    else:
        return render_template('home.html')

    

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
                if form.tutor.data == 1:
                    tutor = True
                else:
                    tutor = False
                user = create_user(form.firstname.data, form.lastname.data, form.grade.data, form.email.data, form.password.data, form.tutor.data)
                login_user(user,remember=True)
                session['logged_in'] = True
                session['username'] = form.firstname.data + " " + form.lastname.data
                if user.is_admin():
                    session['admin'] = True
                return redirect(url_for('regular.unconfirmed'))
        else:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('regular.register'))
    else:
        return render_template('register.html', form=form)

@regular.route('/unconfirmed')
@login_required
def unconfirmed():
    return render_template('unconfirmed.html')

@regular.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('regular.verify_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('regular.unconfirmed'))

@regular.route('/verify/<token>')
def verify_email(token):
    tokenemail = confirm_token(token)

    if tokenemail is False:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('regular.home'))

    user = User.query.filter_by(email = tokenemail).first()
    if user:
        user.confirmed = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')

    return redirect(url_for('regular.home'))

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