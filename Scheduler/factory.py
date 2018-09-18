from Scheduler.login import login_manager
from Scheduler.model import db
from flask import Flask
import os

app = Flask(__name__)

def create_app(config_object, register_blueprint=True):
    app.config.from_object(config_object)
    if register_blueprint:
        from Scheduler.regular import regular
        from Scheduler.announcement import announcement
        from Scheduler.schedule import schedule
        app.register_blueprint(regular)
        app.register_blueprint(announcement)
        app.register_blueprint(schedule)

def extensions():
    login_manager.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()