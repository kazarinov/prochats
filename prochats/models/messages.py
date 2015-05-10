# -*- coding: utf-8 -*-

from .. import db
from .tags import Tag


class TagsMessages(db.Model):
    __tablename__ = 'tags_messages'

    tags_message_id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    tag_id = db.Column(db.BigInteger, db.ForeignKey('tags.tag_id'), nullable=False)
    message_id = db.Column(db.BigInteger, nullable=False)

    tag = db.relationship(Tag, backref=db.backref('tags_messages', lazy='dynamic'))
