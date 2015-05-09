# coding=utf-8

import datetime
from .. import db
from .users import User


class Advertisement(db.Model):
    __tablename__ = 'advertisements'

    STATUS_ACTIVE = 0
    STATUS_ARCHIVED = 1

    advertisement_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price_per_show = db.Column(db.Float, nullable=False)
    budget = db.Column(db.Float)
    active = db.Column(db.Boolean, default=False, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    modify_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                            nullable=False)
    targeted_country = db.Column(db.String(255))
    targeted_region = db.Column(db.String(255))
    targeted_city = db.Column(db.String(255))
    status = db.Column(db.Integer, default=STATUS_ACTIVE, nullable=False)

    user = db.relationship(User, backref=db.backref('advertisements', lazy='dynamic'))

    @property
    def archived(self):
        return self.status == self.STATUS_ARCHIVED


advertisement_tags = db.Table(
    'advertisement_tags', db.metadata,
    db.Column('advertisement_id', db.Integer, db.ForeignKey('advertisements.advertisement_id')),
    db.Column('tag_id', db.BigInteger, db.ForeignKey('tags.tag_id'))
)


class Tag(db.Model):
    __tablename__ = 'tags'

    tag_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    advertisements = db.relationship(Advertisement, secondary=advertisement_tags, lazy='dynamic',
                                     backref=db.backref('tags', lazy='dynamic'))

    @classmethod
    def get_or_create(cls, name):
        existing = cls.query.filter(cls.name == name).first()
        if existing:
            return existing
        return Tag(name=name)


class AdPlatformTarget(db.Model):
    __tablename__ = 'ad_platforms'

    advertisement_id = db.Column(db.Integer, db.ForeignKey('advertisements.advertisement_id'), primary_key=True)
    platform = db.Column(db.String(20), primary_key=True)

    advertisement = db.relationship(Advertisement, backref=db.backref('platforms', lazy='dynamic'))


class AdOsTarget(db.Model):
    __tablename__ = 'ad_os'

    advertisement_id = db.Column(db.Integer, db.ForeignKey('advertisements.advertisement_id'), primary_key=True)
    os = db.Column(db.String(20), primary_key=True)

    advertisement = db.relationship(Advertisement, backref=db.backref('os', lazy='dynamic'))


class AdVersionTarget(db.Model):
    __tablename__ = 'ad_versions'

    advertisement_id = db.Column(db.Integer, db.ForeignKey('advertisements.advertisement_id'), primary_key=True)
    version = db.Column(db.String(20), primary_key=True)

    advertisement = db.relationship(Advertisement, backref=db.backref('versions', lazy='dynamic'))
