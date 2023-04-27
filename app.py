import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'marvelous'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marvel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
upload_folder = os.path.join('static', 'img')
app.config['UPLOAD'] = upload_folder

login_manager = LoginManager()
login_manager.init_app(app)
