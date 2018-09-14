from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email
from Scheduler.model import db, User

class RegisterForm(Form):
    firstname = StringField("First Name",  [InputRequired("Please Enter Your First Name")])
    lastname = StringField("Last Name",  [InputRequired("Please Enter Your Last Name")])
    grade = IntegerField("Grade Level", [InputRequired("Please Enter Your Grade Level")])
    email = StringField("Email",  [InputRequired("Please Enter Your Email Address"), Email("This Field Requires a Valid Email Address")])
    password = PasswordField("Password", [InputRequired("Please Enter Your Password")] )
    confirmpassword = PasswordField("Confirm Password", [InputRequired("Please Confirm Your Password")])
    submit = SubmitField("Create account")

class SigninForm(Form):
    email = StringField("Email",  [InputRequired("Please Enter Your Email Address"), Email("Please Enter Your Email Address")])
    password = PasswordField('Password', [InputRequired("Please Enter a Password.")])
    submit = SubmitField("Sign In")

class AnnouncementForm(Form):
    title = StringField('Title', [InputRequired("Please Enter a Title")])
    body = TextAreaField('Body', [InputRequired("Please Enter a Body")])