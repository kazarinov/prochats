# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('prochats.settings.config')
app.jinja_env.globals["project_name"] = "ProChats"

db = SQLAlchemy(app)

from . import models
from . import views
