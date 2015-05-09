# -*- coding: utf-8 -*-

import os
import logging
import sys

os.environ['TZ'] = 'Europe/Moscow'


class Config(object):
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False  # TODO learn how to use it

    SECRET_KEY = '\xde \xfas|\x99\xe3,\xf5\xf4n\xfb\x10\x80\xfd{\xb0\xb4#:%\xbd\x8a\x99'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': logging.INFO,
            'handlers': ['app_file', 'console'],
        },
        'formatters': {
            'verbose': {
                'format': '[%(asctime)s] %(process)d/%(thread)d %(levelname)s %(name)s %(filename)s:%(lineno)s %(message)s',
            },
            'simple': {
                'format': '%(asctime)s %(process)d/%(thread)d %(levelname)s %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {
            'console': {
                'level': logging.INFO,
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                "stream": sys.stdout
            },
            "app_file": {
                'level': logging.INFO,
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': './logs/interface.log',
                'filters': [
                    'sqlalchemy.engine'
                ]
            },
            "app_traceback": {
                'level': logging.ERROR,
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': './logs/interface-error.log',
                'filters': [

                ]
            },
            "ga_fail": {
                'level': logging.ERROR,
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': './logs/ga-error.log'
            },
            "ga_file": {
                'level': logging.DEBUG,
                'class': 'logging.FileHandler',
                'formatter': 'simple',
                'filename': './logs/ga.log'
            }
        },
        'loggers': {
            'gunicorn.error': {
                'level': logging.DEBUG,
                # 'handlers': ['app_file'],
                'propagate': False
            },
            'gunicorn.access': {
                'level': logging.DEBUG,
                # 'handlers': ['app_file'],
                'propagate': False
            },
            'app': {
                'level': logging.DEBUG,
                'handlers': ['app_file'],
                'propagate': False
            },
            'sqlalchemy': {
                'level': logging.WARNING,
                'propagate': False
            },
            'sqlalchemy.engine': {
                'level': logging.WARNING,
                'propagate': False
            },
            'dmp.ga': {
                'level': logging.DEBUG,
                'handlers': ['ga_file'],
                'propagate': False
            },
            'dmp.ga.error': {
                'level': logging.ERROR,
                'handlers': ['ga_fail', 'console'],
                'propagate': False
            }
        }
    }


class LocalConfig(Config):

    DEBUG = True

    DB_NAME = "prochats"
    DB_USER = "dev"
    DB_PASSWORD = "devdev"
    DB_HOST = "localhost"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../prochats.db'


class RemoteConfig(Config):

    DB_NAME = "prochats"
    DB_USER = "dev"
    DB_PASSWORD = "devdev"
    DB_HOST = "178.62.156.72"

    SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_NAME + '?charset=utf8'

class DevRemoteConfig(RemoteConfig):
    DEBUG = True

    def __init__(self):
        super(DevRemoteConfig, self).__init__()


config = DevRemoteConfig()
