from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_moment import Moment


app = Flask(__name__)
app.config.from_object(Config)


bootstrap = Bootstrap(app)
moment = Moment(app)


from app import routes
