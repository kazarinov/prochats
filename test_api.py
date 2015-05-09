import os
import prochats
import unittest
import tempfile
import json, copy

class FlaskrTestCase(unittest.TestCase):

    sdk_token = ""
    tag_id = ""

    def setUp(self):
        self.db_fd, prochats.app.config['DATABASE'] = tempfile.mkstemp()
        prochats.app.config['TESTING'] = True
        self.app = prochats.app.test_client()
        prochats.db.create_all()
        rv = self.app.post('/register', data=dict(vk_token='vs12345678'))
        self.__class__.sdk_token = copy.deepcopy(json.loads(rv.data)['token'])

    def tearDown(self):
        self.app.post('/delete', headers={"Authentication": self.__class__.sdk_token, })
        os.close(self.db_fd)
        os.unlink(prochats.app.config['DATABASE'])

    def test_adding_user(self):
        rv = self.app.post('/register', data=dict(vk_token='vs12345678'))
        token = json.loads(rv.data)['token']
        assert rv.status_code == 200
        self.app.post('/delete', headers={"Authentication": token, })

    def test_updating_user(self):
        rv = self.app.post('/update', headers={"Authentication": self.__class__.sdk_token, }, data=dict(vk_token='vs12345679'))
        assert rv.status_code == 200
        # Cleaning records in DB

    def test_adding_tag(self):
        rv = self.app.post('/tags/', headers={"Authentication": self.__class__.sdk_token, }, data=dict(
            tag_name="Sample", chat_id=1, mark="interesting"))
        self.__class__.tag_id = copy.deepcopy(json.loads(rv.data)['tag_id'])
        assert rv.status_code == 200

    def test_editing_tag(self):
        rv = self.app.put('/tags/', headers={"Authentication": self.__class__.sdk_token, }, data=dict(
            tag_id=self.__class__.tag_id, mark="flood"))
        assert rv.status_code == 200

    def test_removing_tag(self):
        rv = self.app.delete('/tags/', headers={"Authentication": self.__class__.sdk_token, }, data=dict(
            tag_id=self.__class__.tag_id,))
        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()
