from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from Scheduler.model import db, Announcement
from Scheduler.forms import AnnouncementForm
from Scheduler.decorators import admin_required
from sqlalchemy import func
from sqlalchemy import and_
import datetime
import calendar
import sys

announcement = Blueprint('announcement', __name__, template_folder='templates')

def create_announcement(title, author, body):
    newAnnouncement = Announcement(title, author, body)
    db.session.add(newAnnouncement)
    db.session.commit()
    return newAnnouncement

def delete_announcement(id):
    announcement = Announcement.query.filter_by(id=id).first()
    db.session.delete(announcement)
    db.session.commit()

@announcement.route('/announcements')
def announcements():
    session['month'] = None
    announcements = Announcement.query.all()
    list.reverse(announcements)
    if len(announcements) > 0:
        return render_template('announcements.html', announcements=announcements)
    else:
        msg = 'No Announcements Found'
        return render_template('announcements.html', msg=msg)

@announcement.route('/announcement/<string:id>/')
def view_announcement(id):
    announcement = Announcement.query.filter_by(id=id).first()
    return render_template('announcement.html', announcement=announcement)

@announcement.route('/add_announcement', methods=['GET', 'POST'])
@admin_required
def add_announcement():
    form = AnnouncementForm(request.form)
    if form.validate_on_submit():
        create_announcement(form.title.data, session['username'], form.body.data)
        flash('Announcement created!', 'success')
        return redirect(url_for('regular.dashboard'))
    return render_template('add_announcement.html', form=form)

@announcement.route('/edit_announcement/<string:id>/', methods=['GET', 'POST'])
@admin_required
def edit_announcement(id):
    announcement = Announcement.query.filter_by(id=id).first()
    form = AnnouncementForm(request.form)
    form.title.data = announcement.title
    form.body.data = announcement.body

    if form.validate_on_submit():
        delete_announcement(announcement.id)
        title = request.form['title']
        body = request.form['body']

        create_announcement(title, session['username'], body)

        flash('Announcement edited!', 'success')
        
        return redirect(url_for('regular.dashboard'))
    return render_template('edit_announcement.html', form=form)

@announcement.route('/delete_announcement/<string:id>/')
@admin_required
def delete_route(id):
    delete_announcement(id)
    flash('Announcement Deleted!', 'success')
    return redirect(url_for('regular.dashboard'))