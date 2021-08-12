import os
from flask_mail import Mail


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '5585ed0f-0277-45bf-be40-5e489f70db52'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'nwelter1@gmail.com'

mail = Mail()