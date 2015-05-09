# -*- coding: utf-8 -*-
import datetime

from .. import db, app
from ..models.users import User
from .rendering import to_json, get_renderer
from .validators import (
    accept,
    param_string,
    param_float,
    param_int,
    param_sdk_token,
)
import hashlib, random, sys, datetime


renderer = get_renderer()

@app.route("/register", methods=["POST"])
@to_json
@accept(
    param_string('vk_token', forward='vk_id')
)
def register(vk_id):
    # Генерируем токен уникального приложения
    sdk_token = hashlib.md5(str(random.randint(0, sys.maxint)))
    while (User.query.filter_by(sdk_token=sdk_token).first()):
        sdk_token = hashlib.md5(str(random.randint(0, sys.maxint)))
    new_user = User(vk_token=vk_id, sdk_token=sdk_token)
    db.session.add(new_user)
    db.session.commit()

@app.route("/tags", methods=["GET"])
@to_json
@accept(
    param_sdk_token(),
    param_int('chat_id', forward='chat_id'),
    param_int('message_id', required=None, forward='last_message_id')
)
def get_tags(application, chat_id, last_message_id):
    # Вернуть теги
    pass

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
