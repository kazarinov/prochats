# -*- coding: utf-8 -*-

import hashlib
import random
import sys
import datetime

from .. import db, app
from ..models.users import User
from ..models.tags import Tag
from .rendering import to_json, get_renderer
from .validators import (
    accept,
    param_string,
    param_int,
    param_sdk_token,
)
import vk


renderer = get_renderer()

@app.route("/register", methods=["POST"])
@to_json
@accept(
    param_string('vk_token', forward='vk_id')
)
def register(vk_id):
    # Генерируем токен уникального приложения
    sdk_token = hashlib.sha256(str(random.randint(0, sys.maxint)))
    new_user = User(vk_token=vk_id, sdk_token=sdk_token)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return renderer.error("Server error", 500, e.message)
    else:
        return renderer.client_info(new_user)


def get_vk_messages(vk_token, chat_id, timestamp=None):
    vk_api = vk.API(access_token=vk_token, timeout=5)

    chunk = 200
    result_messages = []

    while True:
        history = vk_api.messages.getHistory(chat_id=chat_id, count=chunk)

        for item in history.get('items'):
            if (timestamp is not None and item.get('date') < timestamp) \
                    or item.get('read_state') == 1 and timestamp is None:
                break

            result_messages.append({
                'body': item.get('body'),
                'message_id': item.get('id'),
                'date': item.get('date'),
                'read_state': item.get('read_state'),
            })

        if history.get('count') < chunk:
            break

    return result_messages


@app.route("/update", methods=["POST"])
@to_json
@accept(
    param_sdk_token(),
    param_string('vk_token', forward='new_vk_id')
)
def update(user, new_vk_id):
    user.vk_id = new_vk_id
    try:
        db.session.commit()
    except Exception as e:
        return renderer.error("Server error", 500, e.message)
    else:
        return renderer.client_info(user)

# Служебная функция: только для тестирования!
@app.route("/delete", methods=["POST"])
@to_json
@accept(
    param_sdk_token(),
)
def delete(user):
    try:
        user.query.delete()
        db.session.commit()
    except Exception as e:
        return renderer.error("Server error", 500, e.message)
    else:
        return renderer.status()

@app.route("/tags", methods=["GET"])
@to_json
@accept(
    param_sdk_token(),
    param_int('chat_id'),
    param_int('timestamp', required=None)
)
def get_tags(user, chat_id, timestamp):
    # получить пачку сообщений для генерации тегов
    messages = get_vk_messages(user.vk_token, chat_id, timestamp)
    tags = {}

    for message in messages:
        for word in message['body'].split():
            if len(word) > 3:
                tag_messages = tags.setdefault(normalize_word(word), [])
                tag_messages.append(message.get('message_id'))

    def compare(a, b):
        if len(tags[a]) > len(tags[b]):
            return 1
        if len(tags[a]) < len(tags[b]):
            return -1
        else:
            return 0

    sorted_dict = sorted(tags, cmp=compare, reverse=True)
    for key in sorted_dict:
        t = Tag(user_id=user.user_id, chat_id=chat_id, name=key, mark='unknown', create_date=datetime.datetime.now())
        db.session.add(t)
    db.session.commit()

    return sorted_dict[:20]

@app.route("/messages", methods=["GET"])
@to_json
@accept(
    param_sdk_token(),
    param_int('chat_id', forward='chat_id'),
    param_string('tag_ids', forward='tags_source')
)
def get_messages(application, chat_id, tags_source):
    # Вернуть сообщения по тегам
    pass

@app.route("/tags/", methods=["PUT"])
@to_json
@accept(
    param_sdk_token(),
    param_int('tag_id', forward='tag_id'),
    param_string('mark', forward='new_mark')
)
def edit_tag(user, tag_id, new_mark):
    tag = Tag.query.filter_by(tag_id=tag_id).first()
    if tag:
        tag.mark = new_mark
        try:
            db.session.commit()
        except Exception as e:
            return renderer.error("Server error", 500, e.message)
        else:
            return renderer.status()
    else:
        return renderer.error("Client error", 404, "Tag not found")

@app.route("/tags/", methods=["POST"])
@to_json
@accept(
    param_sdk_token(),
    param_string('tag_name', forward='tag_name'),
    param_int('chat_id', forward='chat_id'),
    param_string('mark', default='interesting', forward='new_mark')
)
def add_tag(user, tag_name, chat_id, new_mark):
    new_tag = Tag(user_id=user.user_id, chat_id=chat_id, name=tag_name, mark=new_mark)
    try:
        db.session.add(new_tag)
        db.session.commit()
    except Exception as e:
        return renderer.error("Server error", 500, e.message)
    else:
        return renderer.new_tag(new_tag)

@app.route("/tags/", methods=["DELETE"])
@to_json
@accept(
    param_sdk_token(),
    param_int('tag_id', forward='tag_id')
)
def delete_tag(user, tag_id):
    tag = Tag.query.filter_by(tag_id=tag_id).first()
    if tag:
        try:
            tag.query.delete()
            db.session.commit()
        except Exception as e:
            return renderer.error("Server error", 500, e.message)
        else:
            return renderer.status()
    else:
        return renderer.error("Client error", 404, "Tag not found")
