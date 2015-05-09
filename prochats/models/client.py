# -*- coding: utf-8 -*-

from .. import db
import datetime
from sqlalchemy.orm import backref

from .ads import Tag


class Client(db.Model):
    __tablename__ = 'clients'
    '''
    Модель клиента
    '''
    id = db.Column(db.BigInteger, primary_key=True)
    client_id = db.Column(db.String(255))
    age = db.Column(db.SmallInteger)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    '''
    0 - inactive
    1 - active
    '''
    status = db.Column(db.SmallInteger, default=1)

    def is_active(self):
        return self.status == 1


class ClientDevice(db.Model):
    __tablename__ = 'client_devices'

    id = db.Column(db.BigInteger, primary_key=True)
    device_id = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.BigInteger, db.ForeignKey('clients.id'), nullable=False)
    platform = db.Column(db.String(255))
    type = db.Column(db.String(255))
    version = db.Column(db.String(255))
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    client = db.relationship(Client, backref=backref('devices', lazy='dynamic'))


class ClientLocation(db.Model):
    __tablename__ = 'client_locations'

    id = db.Column(db.BigInteger, primary_key=True)
    client_id = db.Column(db.BigInteger, db.ForeignKey('clients.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    client = db.relationship(Client, backref=backref('locations', lazy='dynamic'))


class ClientTag(db.Model):
    __tablename__ = 'client_tags'

    id = db.Column(db.BigInteger, primary_key=True)
    client_id = db.Column(db.BigInteger, db.ForeignKey('clients.id'), nullable=False)
    tag_id = db.Column(db.BigInteger, db.ForeignKey('tags.tag_id'), nullable=False)

    weight = db.Column(db.Float(precision=4), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

    client = db.relationship(Client, backref=backref('tags', lazy='dynamic'))
    tag = db.relationship(Tag, backref=backref('clients', lazy='dynamic'))


class ClientEventTag(db.Model):
    __tablename__ = 'client_event_tags'

    id = db.Column(db.BigInteger, primary_key=True)
    client_id = db.Column(db.BigInteger, db.ForeignKey('clients.id'), nullable=False)
    app_event_id = db.Column(db.BigInteger, nullable=False) #db.ForeignKey('app_events.app_event_id')
    tag_id = db.Column(db.BigInteger, db.ForeignKey('tags.tag_id'), nullable=True)
    static = db.Column(db.Boolean, default=True, nullable=False)

    client = db.relationship(Client, backref=backref('event_tags', lazy='dynamic'))
