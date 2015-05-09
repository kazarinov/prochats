# -*- coding: utf-8 -*-

import datetime

from .. import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    vk_token = db.Column(db.String(255), nullable=False)
    sdk_token = db.Column(db.String(255), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
