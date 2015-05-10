# -*- coding: utf-8 -*-
from functools import wraps

from flask import json, make_response, Response

from . import errors


ERRORS = {
    errors.MissingArgument: (400, 'missing_argument'),
    errors.InvalidArgument: (400, 'invalid_argument'),
    errors.EmptyArgument: (400, 'empty_argument'),
    errors.NotFound: (404, 'not_found'),
    errors.TokenError: (401, 'invalid_token'),
    errors.ApiError: (400, 'api_error'),
    errors.RegistrationError: (400, 'registration_error'),
    errors.UserAlreadyExists: (400, 'user_already_exists'),
    errors.UnauthorizedUser: (401, 'unauthorized'),
}


def get_renderer():
    return Renderer()


def to_json(f):
    '''
    Декоратор преобразует ответ в json
    Декорируемая функция может возвращать текст ответа или tuple (response, status)
    '''
    renderer = get_renderer()

    @wraps(f)
    def wrapper(*args, **kwargs):
        status = 200
        try:
            response = f(*args, **kwargs)
        except Exception, e:
            status, alias = ERRORS.get(e.__class__, (None, None))
            if status:
                response = renderer.error(str(e), status, alias)
            else:
                raise

        if isinstance(response, tuple):
            response, status = response

        if isinstance(response, Response):
            return response
        else:
            response_json = json.dumps(response)
            return make_response(response_json, status, {'Content-type': 'application/json; charset=UTF-8'})

    return wrapper


class Renderer(object):
    @staticmethod
    def error(message, status_code, alias):
        return {
            'status': {
                'code': status_code,
                'message': message,
                'alias': alias,
            }
        }

    @staticmethod
    def status(status='ok'):
        return {
            'status': {
                'code': 0,
                'message': status,
            }
        }

    @staticmethod
    def client_info(user):
        response = {
            'token': user.sdk_token,
        }
        response.update(Renderer.status('ok'))
        return response

    @staticmethod
    def register_info(hash):
        return {
            'token': hash,
            'status': {
                'code': "0"
            },
            'message': 'Success!'
        }

    @staticmethod
    def new_tag(tag):
        response = {
            'tag_id': tag.tag_id,
        }
        response.update(Renderer.status('ok'))
        return response

    @staticmethod
    def tags_messages(tags_messages):
        response = {
            'messages': []
        }
        response.update(Renderer.status('ok'))
        for message in tags_messages:
            response['messages'].append({
                'message_id': message.message_id,
                'tag_id': message.tag_id,
                'tag_name': message.tag.name
            })
        return response

    def tags(self, tags):
        response = {
            'tags': []
        }
        response.update(Renderer.status('ok'))
        for tag in tags:
            response['tags'].append({
                'tag_id': tag.tag_id,
                'name': tag.name,
                'mark': tag.mark,
            })
        return response
