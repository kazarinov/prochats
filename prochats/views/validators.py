# -*- coding: utf-8 -*-
from functools import wraps

from flask import request
from .errors import MissingArgument, InvalidArgument, EmptyArgument, TokenError
from ..models.client import Client
from ..models.apps import Application


def accept(*validators):
    def accept_deco(fun):
        @wraps(fun)
        def new_fun(*args, **kw):
            kw = reduce(lambda _kw, validator: validator(kw), validators, kw)
            return fun(*args, **kw)
        return new_fun
    return accept_deco


def get_param(name, params=None, methods=None):
    '''
    @param name
    @param methods [args, get, post, json]")
    '''
    if params is None:
        params = {}

    sources = {
        'args': params,
        'get': request.args,
        'post': request.form,
        'headers': request.headers,
        'json': request.get_json(force=True, silent=True) or {}
    }

    if methods is None:
        methods = sources.keys()

    for method in methods:
        source = sources.get(method, {})
        if method == 'json':
            name_parts = name.split('.')
            print name_parts
            print source
            for name_part in name_parts:
                try:
                    source = source.get(name_part, None)
                except AttributeError:
                    return None
            return source
        else:
            if source.get(name) is not None:
                return source.get(name)

    return None


def param_body(params):
    if not request.data:
        raise InvalidArgument('body', request.data, 'Body cannot be empty')

    params['body'] = request.data
    return params


def param_bool(name, default=None, methods=None, forward=None):
    def validator(params):
        if forward:
            var_name = forward
        else:
            var_name = name

        value = get_param(name, params, methods)
        if isinstance(value, bool):
            params[var_name] = value
        elif value is None and default is None:
            raise MissingArgument(name)
        elif value is None and default is not None:
            params[var_name] = default
        else:
            value = value.lower()
            if value not in ['true', 'false', '0', '1']:
                raise InvalidArgument(name, value, "Param must be boolean (`true`, `false`, 0, 1)")
            else:
                if value == 'true':
                    params[var_name] = True
                elif value == 'false':
                    params[var_name] = False
                else:
                    params[var_name] = bool(int(value))
        return params
    return validator


def param_string(name, required=True, not_empty=False, methods=None, forward=None):
    def validator(params):
        param_raw = get_param(name, params, methods)
        if forward:
            var_name = forward
        else:
            var_name = name

        if param_raw is None and required:
            raise MissingArgument(name)
        elif param_raw is None and not required:
            params[var_name] = None
            return params

        try:
            param = param_raw.decode('utf-8')
            param = param.strip()
        except Exception, e:
            raise InvalidArgument(name, param_raw, e)

        if not_empty and not param:
            raise EmptyArgument(name)

        params[var_name] = param
        return params

    return validator


def param_num(name, type_func, required=True, methods=None, min_value=None, forward=None):
    def validator(params):
        if forward:
            var_name = forward
        else:
            var_name = name

        param_raw = get_param(name, params, methods)

        if param_raw is None and required:
            raise MissingArgument(name)
        elif param_raw is None and not required:
            params[var_name] = None
            return params
        else:
            try:
                param = type_func(param_raw)
            except ValueError, e:
                raise InvalidArgument(name, param_raw, e)

            if min_value is not None and param < min_value:
                raise InvalidArgument(name, param_raw, 'argument is less than minimum % s!' % min_value)
        params[var_name] = param
        return params

    return validator


def param_int(name, required=True, methods=None, min_value=None, forward=None):
    return param_num(name, int, required, methods, min_value, forward)


def param_float(name, required=True, methods=None, min_value=None, forward=None):
    return param_num(name, float, required, methods, min_value, forward)


def param_file(name, required=True):
    def validator(params):
        param_raw = request.files.get(name)
        print param_raw
        if param_raw is None and required:
            raise MissingArgument(name)
        elif param_raw is None and not required:
            params[name] = None
            return params
        elif required and not param_raw:
            raise EmptyArgument(name)

        params[name] = param_raw
        return params

    return validator


def param_id(name, forward, entity, required=True, methods=None):
    def validator(params):
        param_raw = get_param(name, params, methods)

        if param_raw is None and required:
            raise MissingArgument(name)
        elif param_raw is None and not required:
            params[forward] = None
            return params

        try:
            p_id = int(param_raw)
        except ValueError, e:
            raise InvalidArgument(name, param_raw, e)
        param = entity.query.get(p_id)
        if param is None:
            raise InvalidArgument(name, param_raw,
                                  'There is no row in %s table, corresponding to the given id' % str(entity))

        if params and (not methods or 'args' in methods) and name in params.keys():
            params.pop(name)
        params[forward] = param
        return params

    return validator


def param_enum(name, choice, required=True, methods=None):
    def validator(params):
        param_raw = get_param(name, params, methods)

        if param_raw is None and required:
            raise MissingArgument(name)
        elif param_raw is None and not required:
            params[name] = None
            return params
        else:
            if param_raw not in choice:
                raise InvalidArgument(name, param_raw)
            else:
                params[name] = param_raw
        return params
    return validator


def propagate(*args):
    def validator(params):
        for arg in args:
            params[arg] = get_param(arg, params)
        return params
    return validator


def param_client(name='client_id', forward='client', methods=None):
    if not methods:
        methods = ['args', 'post', 'json']

    def validator(params):
        client_id = get_param(name, params, methods)

        if client_id is None:
            raise MissingArgument(name)

        client = Client.query.filter_by(client_id=client_id).first()
        if client is None:
            raise InvalidArgument(name, client_id, 'There is no client with such client_id')
        else:
            params[forward] = client
            if params and 'args' in methods and name in params.keys():
                params.pop(name)

        return params
    return validator


def param_sdk_token(name='Authentication', forward='application', methods=None):
    if not methods:
        methods = ['headers']

    def validator(params):
        token = get_param(name, params, methods)

        if token is None:
            raise MissingArgument(name)

        application = Application.query.filter_by(sdk_token=token).first()
        if application is None:
            raise TokenError(token)
        else:
            params[forward] = application
            if params and 'args' in methods and name in params.keys():
                params.pop(name)

        return params
    return validator
