# -*- coding: utf-8 -*-
import pytest
import time

#from rengine import db
#from rengine.models import Client

from . import HTTPTest


SDK_TOKEN = 'MnzecdwxZm2qOVuX1IZ2KIZ3bnXkBw'
INVALID_TOKEN = 'invalid_token'


class TestUser(HTTPTest):
    def test_register(self):
        data = {
            'vk_id': 'qwerty12345'
        }
        status, response = self.assertOk('/register', method='POST', data=data)
        assert response.get('status') == 'ok'

# class TestUser(HTTPTest):
#     def _create_client(self, client_id):
#         client = Client(
#             client_id=client_id,
#         )
#         self._add_entry(client)
#         return client
#
#     @pytest.fixture
#     def client(self, request):
#         login = str(time.time())
#         client = self._create_client(client_id=login + 'qwerty123456')
#         return client  # provide the fixture value
#
#     @staticmethod
#     def _add_entry(entry):
#         db.session.add(entry)
#         db.session.commit()
#
#     @staticmethod
#     def _delete_entry(entry):
#         db.session.delete(entry)
#         db.session.commit()
#
#
# class TestInitiate(TestUser):
#     def test_initiate_correct(self):
#         login = str(time.time())
#         data = {
#             'client_id': login + 'client_id',
#             'device': {
#                 'device_id': '123456',
#                 'type': 'iphone',
#                 'platform': 'ios',
#                 'version': '8.01'
#             }
#         }
#         status, response = self.assertOk('/client/initiate', method='POST', data=data,
#                                          headers={'Authentication': SDK_TOKEN})
#         assert response.get('status') == 'ok'
#         assert response.get('client', {}).get('id')
#
#     def test_initiate_existing(self):
#         login = str(time.time())
#         data = {
#             'client_id': login + 'client_id',
#             'device': {
#                 'device_id': '123456',
#                 'type': 'iphone',
#                 'platform': 'ios',
#                 'version': '8.01'
#             }
#         }
#         status, response = self.assertOk('/client/initiate', method='POST', data=data,
#                                          headers={'Authentication': SDK_TOKEN})
#         client_id1 = response.get('client', {}).get('id')
#         status, response = self.assertOk('/client/initiate', method='POST', data=data,
#                                          headers={'Authentication': SDK_TOKEN})
#         client_id2 = response.get('client', {}).get('id')
#         assert client_id1 == client_id2
#
#     def test_initiate_no_client_id(self):
#         data = {
#             'device': {
#                 'device_id': '123456',
#                 'type': 'iphone',
#                 'platform': 'ios',
#                 'version': '8.01'
#             }
#         }
#         self.assertStatus('/client/initiate', method='POST', data=data,
#                           headers={'Authentication': SDK_TOKEN})
#
#     def test_initiate_no_device(self):
#         login = str(time.time())
#         data = {
#             'client_id': login + 'client_id'
#         }
#         self.assertStatus('/client/initiate', method='POST', data=data,
#                           headers={'Authentication': SDK_TOKEN})
#
#     def test_initiate_no_device_platform(self):
#         login = str(time.time())
#         data = {
#             'client_id': login + 'client_id',
#             'device': {
#                 'device_id': '123456',
#                 'type': 'iphone',
#                 'version': '8.01'
#             }
#         }
#         self.assertStatus('/client/initiate', method='POST', data=data,
#                           headers={'Authentication': SDK_TOKEN})
#
#     def test_initiate_invalid_token(self):
#         login = str(time.time())
#         data = {
#             'client_id': login + 'client_id',
#             'device': {
#                 'device_id': '123456',
#                 'type': 'iphone',
#                 'platform': 'ios',
#                 'version': '8.01'
#             }
#         }
#         self.assertStatus('/client/initiate', method='POST', data=data,
#                           headers={'Authentication': INVALID_TOKEN}, status=401)
#
#
# class TestUpdateLocation(TestUser):
#     def test_update_location_correct(self, client):
#         data = {
#             'client_id': client.client_id,
#             'location': {
#                 'latitude': '121.033',
#                 'longitude': '89.1212'
#             },
#             'timestamp': time.time()
#         }
#         status, response = self.assertOk('/client/location', method='POST', data=data,
#                                          headers={'Authentication': SDK_TOKEN})
#         assert response.get('status') == 'ok'
#
#     def test_update_location_no_location(self, client):
#         data = {
#             'client_id': client.client_id,
#             'timestamp': time.time()
#         }
#         self.assertStatus('/client/location', method='POST', data=data,
#                           headers={'Authentication': SDK_TOKEN})
#
#     def test_update_location_no_latitude(self, client):
#         data = {
#             'client_id': client.client_id,
#             'location': {
#                 'longitude': '89.1212'
#             },
#             'timestamp': time.time()
#         }
#         self.assertStatus('/client/location', method='POST', data=data,
#                           headers={'Authentication': SDK_TOKEN})
#
#     def test_update_location_invalid_token(self, client):
#         data = {
#             'client_id': client.client_id,
#             'location': {
#                 'latitude': '121.033',
#                 'longitude': '89.1212'
#             },
#             'timestamp': time.time()
#         }
#         self.assertStatus('/client/location', method='POST', data=data,
#                           headers={'Authentication': INVALID_TOKEN}, status=401)
#
#
# class TestGetClientAdvertisements(TestUser):
#     def test_get_client_advertisements_no_ads_correct(self, client):
#         status, response = self.assertOk('/client/advertisements', params={'client_id': client.client_id},
#                                          headers={'Authentication': SDK_TOKEN})
#         assert response.get('status') == 'ok'
#         assert len(response.get('advertisements')) == 0
#
#     def test_get_client_advertisements_invalid_token(self, client):
#         self.assertStatus('/client/advertisements', params={'client_id': client.client_id},
#                           headers={'Authentication': INVALID_TOKEN}, status=401)
