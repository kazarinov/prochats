# coding=utf-8

import datetime
from .. import db


class User(db.Model):
    __tablename__ = 'users'

    TYPE_DEVELOPER = 0
    TYPE_ADVERTISING = 1

    STATUS_ACTIVE = 0
    STATUS_DELETED = 1

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = db.Column(db.Integer, default=STATUS_ACTIVE, nullable=False)
