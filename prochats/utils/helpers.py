# -*- coding: utf-8 -*-
import logging
from functools import wraps
import mimetypes
import mimetools
import time

log = logging.getLogger(__name__)


def retriable_n(retry_count=3, time_sleep=0.2, exceptions=(Exception,)):
    def retriable_n_deco(func):
        @wraps(func)
        def wrapper(*args, **kw):
            for i in range(retry_count - 1):
                try:
                    return func(*args, **kw)
                except Exception, e:
                    if isinstance(e, exceptions):
                        log.warning('%s(*%s, **%s) try %i failed, retrying: %s', func.__name__, args, kw, i, e)
                        time.sleep(time_sleep)
                    else:
                        raise
            else:
                return func(*args, **kw)
        return wrapper
    return retriable_n_deco


retriable = retriable_n()


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def encode_multipart(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    boundary = mimetools.choose_boundary()
    res = []
    for (key, value) in fields:
        res.append('--' + boundary)
        res.append('Content-Disposition: form-data; name="%s"' % key)
        res.append('')
        res.append(str(value))
    for (key, filename, value) in files:
        size = len(value)
        res.append('--' + boundary)
        res.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        res.append('Content-Type: %s' % get_content_type(filename))
        res.append('Content-Length: %s' % size)
        res.append('')
        res.append(value)
    res.append('--' + boundary + '--')
    res.append('')
    body = '\r\n'.join(res)
    content_type = 'multipart/form-data; boundary=%s' % boundary
    return content_type, body


def datetime_to_timestamp(date):
    return int(time.mktime(date.timetuple()))
