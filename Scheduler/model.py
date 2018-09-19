from flask_sqlalchemy import SQLAlchemy
from flask import Flask 
import os
import bcrypt
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    grade = db.Column(db.Integer)
    pw_hash = db.Column(db.String(500))
    salt = db.Column(db.String(100))
    tutor = db.Column(db.Boolean)

    def __init__(self, firstname, lastname, grade, email, password, tutor):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.grade = grade
        self.pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.tutor = tutor

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_annonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
        
    def is_tutor(self):
        if self.tutor == 1:
            return True
        else:
            return False

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.pw_hash.encode('utf-8'))

    def is_admin(self):
        if self.email in ['test@test.com', 'hello@gmail.com', 'admin@admin.com']:
            return True
        else:
            return False

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    author = db.Column(db.String(100))
    create_date = db.Column(db.String(10))
    body = db.Column(db.Text)

    def __init__(self, title, author, body):
        self.title = title.title()
        self.author = author.title()
        self.body = body
        self.create_date = date.today().strftime("%m-%d-%y")
    
class TutoringSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    user = db.Column(db.Integer)
    tutor = db.Column(db.Integer)
    subject = db.Column(db.String(50))
    comments = db.Column(db.Text)
    time = db.Column(db.String(20))

    def __init__(self, date, subject, comments, user, time):
        self.date = date
        self.subject = subject.title()
        self.comments = comments
        self.user = user
        self.time = time

    def student_name(self):
        student = User.query.filter_by(id=self.user).first()
        return student.firstname + ' ' + student.lastname