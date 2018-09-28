from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, PasswordField, BooleanField, IntegerField, SelectField, DateTimeField, DateField
from wtforms.validators import InputRequired, Email
from Scheduler.model import db, User

class RegisterForm(FlaskForm):
    firstname = StringField("First Name",  [InputRequired("Please Enter Your First Name")])
    lastname = StringField("Last Name",  [InputRequired("Please Enter Your Last Name")])
    grade = SelectField("Grade Level", [InputRequired("Please Enter Your Grade Level")], choices=[(9, 9), (10, 10), (11, 11), (12, 12)], coerce=int)
    email = StringField("Email", [InputRequired("Please Enter Your Email Address"), Email("This Field Requires a Valid Email Address")])
    tutor = SelectField("Are you a tutor or student?", choices=[(1, 'Tutor'), (0, 'Student')], coerce=int)
    password = PasswordField("Password", [InputRequired("Please Enter Your Password")] )
    confirmpassword = PasswordField("Confirm Password", [InputRequired("Please Confirm Your Password")])
    submit = SubmitField("Create Account")

class SigninForm(FlaskForm):
    email = StringField("Email", [Email("Please Enter Your Email Address")])
    password = PasswordField('Password', [InputRequired("Please Enter a Password.")])

class AnnouncementForm(FlaskForm):
    title = StringField('Title', [InputRequired("Please Enter a Title")])
    body = TextAreaField('Body', [InputRequired("Please Enter a Body")])

class EventForm(FlaskForm):
    subject = SelectField('Subject', [InputRequired("Please Select the Subject")], choices=[('math', 'Math'), ('history', 'History'), ('science', 'Science')], coerce=str)
    comments = TextAreaField('Comments')