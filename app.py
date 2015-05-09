# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('prochats.settings.config')
app.jinja_env.globals["project_name"] = "ProChats"

db = SQLAlchemy(app)

api = Api(app, prefix='/api', catch_all_404s=True)
api.unauthorized = lambda resp: resp  # disable basic auth request

from prochats import views

if __name__ == '__main__':
    app.run()