# -*- coding: utf-8 -*-
import hashlib
import random
import sys
import datetime
import re

import vk
from vk import VkAPIMethodError

from .. import db, app
from ..utils.nlp import normalize_word
from ..utils.helpers import retriable_n
from ..models.users import User
from ..models.tags import Tag
from ..models.messages import TagsMessages
from .rendering import to_json, get_renderer
from .validators import (
    accept,
    param_string,
    param_int,
    param_sdk_token,
    param_id,
)


renderer = get_renderer()


@app.route("/register", methods=["POST"])
@to_json
@accept(
    param_string('vk_token', forward='vk_id')
)
def register(vk_id):
    # Генерируем токен уникального приложения
    sdk_token = hashlib.sha256(str(random.randint(0, sys.maxint)))
    #sdk_token = "abc"
    try:
        new_user = User(vk_token=vk_id, sdk_token=sdk_token)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return renderer.error("Server error", 500, e.message)
    else:
        return renderer.register_info(sdk_token)


@retriable_n(retry_count=3, time_sleep=1, exceptions=(VkAPIMethodError, ))
def get_vk_history(vk_api, chat_id, start_message_id, count):
    return vk_api.messages.getHistory(chat_id=chat_id, start_message_id=start_message_id, count=count)


def get_vk_messages(vk_token, chat_id, timestamp=None):
    vk_api = vk.API(access_token=vk_token, timeout=5)

    chunk = 200
    result_messages = []
    start_message_id = -1
    finish = False

    while True:
        history = get_vk_history(vk_api, chat_id=chat_id, start_message_id=start_message_id, count=chunk)

        for item in history.get('items'):
            print item.get('date'), timestamp
            if (timestamp is not None and item.get('date') < timestamp) \
                    or item.get('read_state') == 1 and timestamp is None:
                finish = True
                break

            result_messages.append({
                'body': item.get('body'),
                'message_id': item.get('id'),
                'date': item.get('date'),
                'read_state': item.get('read_state'),
            })

        if finish or history.get('count') < chunk:
            break
        else:
            start_message_id = history.get('items')[-1]['id']

    return result_messages


@app.route("/update", methods=["POST"])
@to_json
@accept(
    param_sdk_token(),
    param_string('vk_token', forward='new_vk_id')
)
def update(user, new_vk_id):
    user.vk_id = new_vk_id
    db.session.commit()
    return renderer.client_info(user)


# Служебная функция: только для тестирования!
@app.route("/delete", methods=["POST"])
@to_json
@accept(
    param_sdk_token(),
)
def delete(user):
    user.query.delete()
    db.session.commit()
    return renderer.status()


@app.route("/tags", methods=["GET"])
@to_json
@accept(
    param_sdk_token(),
    param_int('chat_id'),
    param_int('timestamp', required=None),
)
def get_tags(user, chat_id, timestamp):
    # получить пачку сообщений для генерации тегов
    limit = 20
    messages = get_vk_messages(user.vk_token, chat_id, timestamp)
    tags = {}

    for message in messages:
        for word in message['body'].split():
            # remove punctuation
            n_word = re.sub('$[,.:!?]', '', re.sub('[,.:!$?]', '', word))
            normal_word = normalize_word(n_word)
            if normal_word:
                tag_messages = tags.setdefault(normalize_word(n_word), [])
                tag_messages.append(message.get('message_id'))

    def compare(a, b):
        if len(tags[a]) > len(tags[b]):
            return 1
        if len(tags[a]) < len(tags[b]):
            return -1
        else:
            return 0

    sorted_dict = sorted(tags, cmp=compare, reverse=True)
    tags_objects = []
    for key in sorted_dict[:limit]:
        tag = Tag(
            user_id=user.user_id,
            chat_id=chat_id,
            name=key,
            mark='unknown',
            create_date=datetime.datetime.now(),
        )
        db.session.add(tag)
        db.session.commit()
        tags_objects.append(tag)

        for message_id in tags[key]:
            db.session.add(
                TagsMessages(tag_id=tag.tag_id, message_id=message_id)
            )
        db.session.commit()

    return renderer.tags(tags_objects)


@app.route("/messages", methods=["GET"])
@to_json
@accept(
    param_sdk_token(),
    param_int('chat_id', forward='chat_id'),
    param_string('tag_ids', forward='tags_ids')
)
def get_messages(user, chat_id, tags_ids):
    # Вернуть сообщения по тегам
    tags_messages = TagsMessages.query.filter(TagsMessages.tag_id.in_(tags_ids.split()))
    return renderer.tags_messages(tags_messages)


@app.route("/tags", methods=["PUT"])
@to_json
@accept(
    param_sdk_token(),
    param_id('tag_id', forward='tag', entity=Tag),
    param_string('mark', forward='new_mark')
)
def edit_tag(user, tag, new_mark):
    tag.mark = new_mark
    db.session.commit()
    return renderer.status()


@app.route("/tags", methods=["POST"])
@to_json
@accept(
    param_sdk_token(),
    param_string('tag_name', forward='tag_name'),
    param_int('chat_id'),
    param_string('mark', default='interesting')
)
def add_tag(user, tag_name, chat_id, mark):
    new_tag = Tag(
        user_id=user.user_id,
        chat_id=chat_id,
        name=tag_name,
        mark=mark,
    )
    db.session.add(new_tag)
    db.session.commit()
    return renderer.new_tag(new_tag)


@app.route("/tags", methods=["DELETE"])
@to_json
@accept(
    param_sdk_token(),
    param_id('tag_id', forward='tag', entity=Tag)
)
def delete_tag(user, tag):
    tag.query.delete()
    db.session.commit()
    return renderer.status()
