# -*- coding: utf-8 -*-

import datetime

from .. import db
from .users import User


class Tag(db.Model):
    __tablename__ = 'tags'

    tag_id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    chat_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    mark = db.Column(db.Enum('unknown', 'flood', 'interesting'), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = db.relationship(User, backref=db.backref('tags', lazy='dynamic'))
