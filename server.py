from Scheduler.factory import create_app, extensions, app
from Scheduler.config import ProductionConfig
from gevent.pywsgi import WSGIServer

create_app(ProductionConfig)
extensions()

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()