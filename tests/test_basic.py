import unittest
import os
import json
from app import app
import const


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        if os.path.exists('db'):
            os.remove('db')

    def test_get_empty(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def start(self):
        return self.app.post('/game', data=json.dumps({"user_id": 3, "answer": "/start"}),
                             content_type="application/json")

    def negative_answer(self):
        return self.app.post('/game', data=json.dumps({"user_id": 3, "answer": "нет"}),
                             content_type="application/json")

    def positive_answer(self):
        return self.app.post('/game', data=json.dumps({"user_id": 3, "answer": "да"}),
                             content_type="application/json")

    def test_post_start(self):
        result = self.start()
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data.decode('UTF-8'), const.WELCOME_MESSAGE)

    def test_post_fin_state1(self):
        self.start()
        result = self.negative_answer()
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data.decode('UTF-8'), const.NOT_BREAD_MESSAGE)

    def test_post_fin_state2(self):
        self.start()
        self.positive_answer()
        result = self.positive_answer()
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data.decode('UTF-8'), const.NOT_BREAD_MESSAGE)

    def test_post_fin_state3(self):
        self.start()
        self.positive_answer()
        result = self.negative_answer()
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data.decode('UTF-8'), const.NOT_CAT_MESSAGE)

    def test_post_middle_state(self):
        self.start()
        result = self.positive_answer()
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data.decode('UTF-8'), const.MAYBE_CAT_BREAD_MESSAGE)

    def test_post_after_dialog(self):
        self.start()
        self.negative_answer()
        result = self.negative_answer()
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data.decode('UTF-8'), const.END_GAME_MESSAGE)

    def test_help(self):
        result = self.positive_answer()
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data.decode('UTF-8'), const.HELP_MESSAGE)


if __name__ == '__main__':
    unittest.main()
