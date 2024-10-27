from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

#Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('configuration.ProductionConfig')
app.config.from_object('app.configuration.DevelopmentConfig')
#app.config.from_object('configuration.TestingConfig')

db = SQLAlchemy(app) #flask-sqlalchemy

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

from app import views, models