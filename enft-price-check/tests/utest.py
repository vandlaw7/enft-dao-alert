import unittest
import requests, json

URL = 'http://127.0.0.1:5000/'


def pollHandle_test():
    telegram_answer_1 = {'update_id': 1,
                         'poll_answer':
                             {'poll_id': '6084757438999822346',
                              'user': {'id': 1, 'is_bot': False, 'first_name': 'Changwoo', 'last_name': 'Nam',
                                       'username': 'vandlaw'},
                              'option_ids': [0]}}

    telegram_answer_2 = {'update_id': 2,
                         'poll_answer':
                             {'poll_id': '6084757438999822346',
                              'user': {'id': 2, 'is_bot': False, 'first_name': 'Changwoo', 'last_name': 'Nam',
                                       'username': 'vandlaw'},
                              'option_ids': [0]}}

    requests.post(URL, data=json.dumps(telegram_answer_1))
    print("done 1")
    requests.post(URL, data=json.dumps(telegram_answer_2))
    print("done 2")


pollHandle_test()