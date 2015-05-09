# -*- coding: utf-8 -*-
import json
import urllib
import pytest

from rengine import app as test_app


class HTTPTest(object):
    app = test_app.test_client()

    def _request(self, url, params=None, headers=None, method='GET', data=None, send_json=True):
        if params is None:
            params = {}

        full_url = url + ('?' + urllib.urlencode(params) if params else '')

        if send_json:
            data = json.dumps(data)

        if method == 'GET':
            response = self.app.get(full_url, headers=headers)
        elif method == 'PUT':
            response = self.app.put(full_url, headers=headers, data=data)
        elif method == 'DELETE':
            response = self.app.delete(full_url, headers=headers, data=data)
        else:
            response = self.app.post(full_url, data=data, headers=headers)

        status_parts = response.status.split()
        status = int(status_parts[0])

        try:
            response_json = json.loads(response.data)
            print response_json
            return status, response_json
        except ValueError:
            pytest.fail("Invalid response: %s" % response.data)

    def assertStatus(self, url, params=None, headers=None, method='GET', data=None, status=400, send_json=True):
        if not headers:
            headers = {}
        if not params:
            params = {}
        response_status, response = self._request(url, params, headers, method, data, send_json)
        assert response_status == status
        return response_status, response

    def assertOk(self, url, params=None, headers=None, method='GET', data=None, send_json=True):
        response_status, response = self.assertStatus(url, params, headers, method, data, 200, send_json)
        return response_status, response

    def assertUploadStatus(self, url, data, params=None, headers=None, status=200):
        if not params:
            params = {}
        if not headers:
            headers = {}
        response_status, response = self._request(url, params, headers=headers, method='POST', data=data, send_json=False)
        assert response_status == status
        return response_status, response
