# -*- coding: utf-8 -*-
import hashlib
import random
import sys

import vk
from ..utils.nlp_utils import normalize_word
from .. import db, app
from ..models.users import User
from .rendering import to_json, get_renderer
from .validators import (
    accept,
    param_string,
    param_int,
    param_sdk_token,
)


renderer = get_renderer()

@app.route("/register", methods=["POST"])
@to_json
@accept(
    param_string('vk_token', forward='vk_id')
)
def register(vk_id):
    # Генерируем токен уникального приложения
    sdk_token = hashlib.md5(str(random.randint(0, sys.maxint)))
    while User.query.filter_by(sdk_token=sdk_token).first():
        sdk_token = hashlib.md5(str(random.randint(0, sys.maxint)))
    new_user = User(vk_token=vk_id, sdk_token=sdk_token)
    db.session.add(new_user)
    db.session.commit()


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
        for word in message.split():
            tags[word].append(word)

    return tags


def get_tags_(token, chat_id):
    messages = get_vk_messages(token, chat_id, 1421194251)
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

    for tag in sorted_dict:
        print tag, tags[tag]

    return tags

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
def edit_tag(application, tag_id, new_mark):
    # Изменить статус тега на new_mark
    pass

@app.route("/tags/", methods=["POST"])
@to_json
@accept(
    param_sdk_token(),
    param_string('tag_name', forward='tag_name'),
    param_string('mark', default='interesting', forward='new_mark')
)
def add_tag(application, tag_name, new_mark):
    # Добавить тег с заданным статусом
    pass

@app.route("/tags/", methods=["DELETE"])
@to_json
@accept(
    param_sdk_token(),
    param_int('tag_id', forward='tag_id')
)
def delete_tag(application, tag_id):
    # Удалить тег
    pass
