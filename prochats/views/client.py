# -*- coding: utf-8 -*-
import datetime

from .. import db, app
from ..models.client import ClientLocation, Client, ClientDevice
from .rendering import to_json, get_renderer
from .validators import (
    accept,
    param_string,
    param_client,
    param_float,
    param_int,
    param_sdk_token,
)


renderer = get_renderer()

@app.route("/register", methods=["POST"])
@to_json
@accept(
    param_string('vk_token')
)
def register(vk_id):
    # Добавить в БД, вернуть токен клиента и статус
    pass

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
def edit_tag(application, tag_id):
    # Удалить тег
    pass
