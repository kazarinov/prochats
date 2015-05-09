# -*- coding: utf-8 -*-
import pytest
import time

from prochats import db
from prochats.models import User

from . import HTTPTest


SDK_TOKEN = 'MnzecdwxZm2qOVuX1IZ2KIZ3bnXkBw'
VK_TOKEN = 'c319fd792e1718389df2efc826da358c16b3169d35a510bd5475e943ec0ebd3cc20e7416ca44833681fdd68724bec'


class TestUser(HTTPTest):
    def _create_user(self):
        user = User(
            vk_token=VK_TOKEN,
            sdk_token=SDK_TOKEN,
        )
        self._add_entry(user)
        return user

    @pytest.fixture
    def user(self, request):
        login = str(time.time())
        client = self._create_user()
        return client  # provide the fixture value

    @staticmethod
    def _add_entry(entry):
        db.session.add(entry)
        db.session.commit()

    @staticmethod
    def _delete_entry(entry):
        db.session.delete(entry)
        db.session.commit()


class TestGetTags(TestUser):
    CHAT_ID = 122

    def test_get_tags_correct(self, user):
        params = {
            'chat_id': self.CHAT_ID,
            'timestamp': 0,
        }
        status, response = self.assertOk('/tags', params=params, headers={'Authentication': user.sdk_token})
        assert response.get('status') == 'ok'
        assert len(response.get('tags')) > 0
