from Scheduler.factory import create_app, extensions, app
from gevent.pywsgi import WSGIServer

class Config(object):
    DEBUG = False
    SECRET_KEY = "secret_key"
    SECURITY_PASSWORD_SALT = "security_salt"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../data.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../data.db'

create_app(ProductionConfig)
extensions()

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()