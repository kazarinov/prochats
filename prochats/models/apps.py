# coding=utf-8

import base64
import datetime
import os
from .. import db
from sqlalchemy import update
from sqlalchemy.exc import OperationalError
from ..utils.helpers import retriable_n
from .users import User
from .ads import Tag


class Application(db.Model):
    __tablename__ = 'applications'

    STATUS_ACTIVE = 0
    STATUS_DELETED = 1

    QUEUE_STATUS_FREE = 0
    QUEUE_STATUS_LOCKED = 1

    app_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    ga_app_id = db.Column(db.String(45), nullable=False)
    ga_email = db.Column(db.String(255), nullable=False)
    ga_client_id_dimension = db.Column(db.String(255), nullable=False)
    sdk_token = db.Column(db.String(45), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    modify_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                            nullable=False)
    status = db.Column(db.Integer, default=STATUS_ACTIVE, nullable=False)
    queue_status = db.Column(db.SmallInteger, default=QUEUE_STATUS_FREE, nullable=False)
    queue_ts = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = db.relationship(User, backref=db.backref('applications', lazy='dynamic'))

    def create_sdk_token(self):
        token_string = "%s|%s" % (self.app_id, os.urandom(20))
        token = base64.urlsafe_b64encode(token_string).strip("=")
        self.sdk_token = token
        return token

    @staticmethod
    @retriable_n(retry_count=3, time_sleep=0.2, exceptions=(OperationalError, ))
    def pop(limit=1, ts=None):
        if ts is None:
            ts = datetime.datetime.now()

        apps = (Application.query
                .filter(Application.status == Application.STATUS_ACTIVE)
                .filter(
                    ((Application.queue_status == Application.QUEUE_STATUS_FREE) & (Application.queue_ts <= ts)) |
                    ((Application.queue_status == Application.QUEUE_STATUS_LOCKED) & (Application.queue_ts <= datetime.datetime.now() - datetime.timedelta(minutes=30)))
                )
                .order_by(Application.queue_ts)
                .limit(limit)
                .with_for_update()
                .all())

        if apps:
            db.session.execute(
                update(Application)
                .values({'queue_status': Application.QUEUE_STATUS_LOCKED, 'queue_ts': ts})
                .where(Application.app_id.in_([app.app_id for app in apps]))
            )
        db.session.commit()
        return apps

    def reset(self):
        self.queue_status = self.QUEUE_STATUS_FREE
        self.queue_ts = datetime.datetime.now()
        db.session.commit()

    def delay(self, ts):
        self.queue_status = self.QUEUE_STATUS_FREE
        self.queue_ts = ts
        db.session.commit()



app_event_tags = db.Table(
    'app_event_tags', db.metadata,
    db.Column('app_event_id', db.Integer, db.ForeignKey('app_events.app_event_id')),
    db.Column('tag_id', db.BigInteger, db.ForeignKey('tags.tag_id'))
)


class AppEvent(db.Model):
    __tablename__ = 'app_events'

    app_event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    event_rule = db.Column(db.Text, nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('applications.app_id'), nullable=False)

    app = db.relationship(Application, backref=db.backref('events', lazy='dynamic'))
    tags = db.relationship(Tag, secondary=app_event_tags, lazy='dynamic',
                           backref=db.backref('app_events', lazy='dynamic'))
