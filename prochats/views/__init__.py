# -*- coding: utf-8 -*-

from flask import render_template, request
from .. import app
from . import client
from rengine.utils import es_api


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/app/")
@app.route("/app/<path:_>")
def web_app(_=""):
    return render_template("web.html")


@app.route("/es/<path:path>")
def es_api_view(path):
    return es_api.get_raw(path, request.args)
