# -*- coding: utf-8 -*-


class ApiError(Exception):
    def __init__(self, message):
        super(ApiError, self).__init__(message)


class MissingArgument(ApiError):
    def __init__(self, name):
        super(MissingArgument, self).__init__('Missing argument %s' % name)
        self.name = name


class EmptyArgument(ApiError):
    def __init__(self, name):
        super(EmptyArgument, self).__init__('Empty argument %s' % name)
        self.name = name


class InvalidArgument(ApiError):
    def __init__(self, name, value, message=''):
        super(InvalidArgument, self).__init__('Invalid argument %s: %s. %s' % (name, value, message))
        self.name = name
        self.value = value


class NotFound(ApiError):
    def __init__(self, entity, id):
        super(NotFound, self).__init__('Not found %s with id %s' % (entity, id))
        self.entity = entity
        self.id = id


class UserAlreadyExists(ApiError):
    def __init__(self, email):
        super(UserAlreadyExists, self).__init__('User with email %s already exists' % email)
        self.email = email


class UserNotFound(ApiError):
    def __init__(self, uid):
        super(UserNotFound, self).__init__('User %s is not found' % uid)


class UnauthorizedUser(ApiError):
    def __init__(self, uid='', message=''):
        super(UnauthorizedUser, self).__init__('Unauthorized user %s %s' % (uid, message))


class RegistrationError(ApiError):
    def __init__(self, error):
        super(RegistrationError, self).__init__('Errors on registration: %s' % error)
        self.error = error


class TokenError(ApiError):
    def __init__(self, token):
        self.token = token
        super(TokenError, self).__init__("Invalid token %s" % self.token)
