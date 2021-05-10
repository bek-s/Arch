from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from sys import platform
from threading import Thread

app = Flask(__name__)
app.secret_key = 'mika_dagestan'
if platform == "linux" or platform == "linux2":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kirill:CasioTitanium1!@localhost/game'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/game'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

from Arch import routes, models, background

skill_back_thread = Thread(target=background.skillup)
skill_back_thread.start()
#working_back_thread = Thread(target=background.end_working())
#working_back_thread.start()
