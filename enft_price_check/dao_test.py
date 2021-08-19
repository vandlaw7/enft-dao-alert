import unittest

import requests
import firebase_admin
from firebase_admin import credentials, firestore
from telegram.ext import Updater

from my_package.polling_bot import token, start_telegram_poll

from my_package.global_var import db
import sys

import logging

log = logging.getLogger(__name__)

data_send = {'name': 'John Smith', 'age': 42, 'employed': False}
data_two = {'category': 'parcel', 'chain': 'ethereum'}
# db.collection(chat_id).document('public_account').set(data_send)
# db.collection(chat_id).document('nft_pendings').collections('123').set('data_two')

# db.collection('dao').document(str(chat_id)).set(data_send)
# db.collection('dao').document(chat_id).collection('nft_pendings').add(data_two)

abc = {'update_id': 861595762,
       'poll_answer':
           {'poll_id': '6310048449567916050',
            'user': {'id': 1743100030, 'is_bot': False, 'first_name': 'Changwoo', 'last_name': 'Nam',
                     'username': 'vandlaw'},
            'option_ids': [1]}}

wow = {'update_id': 861595838,
       'message': {'message_id': 54,
                   'from': {'id': 1743100030, 'is_bot': False, 'first_name': 'Changwoo',
                            'last_name': 'Nam', 'username': 'vandlaw', 'language_code': 'ko'},
                   'chat': {'id': -557391640, 'title': '0721', 'type': 'group',
                            'all_members_are_administrators': True}, 'date': 1626843911,
                   'new_chat_participant': {'id': 1934759690, 'is_bot': True,
                                            'first_name': 'NFTscanner', 'username': 'NFTscannerbot'},
                   'new_chat_member': {'id': 1934759690, 'is_bot': True, 'first_name': 'NFTscanner',
                                       'username': 'NFTscannerbot'}, 'new_chat_members': [
               {'id': 1934759690, 'is_bot': True, 'first_name': 'NFTscanner', 'username': 'NFTscannerbot'}]}}

# requests.post('http://127.0.0.1:5000/daoSetting/', json=dao_update)


# requests.get(
#     'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/'
#     'sendMessage?chat_id=-443191914&text=wowwowowow')

aaa = {'update_id': 861596019, 'message': {'message_id': 111,
                                           'from': {'id': 1743100030, 'is_bot': False, 'first_name': 'Changwoo',
                                                    'last_name': 'Nam', 'username': 'vandlaw', 'language_code': 'ko'},
                                           'chat': {'id': -557391640, 'title': '0721', 'type': 'group',
                                                    'all_members_are_administrators': True}, 'date': 1628310209,
                                           'text': 'Dddd'}}

bbb = {'update_id': 861596050, 'message': {'message_id': 126,
                                           'from': {'id': 1743100030, 'is_bot': False, 'first_name': 'Changwoo',
                                                    'last_name': 'Nam', 'username': 'vandlaw', 'language_code': 'ko'},
                                           'chat': {'id': -443191914, 'title': 'Test', 'type': 'group',
                                                    'all_members_are_administrators': True}, 'date': 1628335706,
                                           'text': '/chatid',
                                           'entities': [{'offset': 0, 'length': 7, 'type': 'bot_command'}]}}

# requests.post('http://127.0.0.1:5000/', json=bbb)

ccc = {'delete_chat_photo': False, 'date': 1628337660,
       'poll': {'explanation_entities': [], 'type': 'regular', 'id': '6084461726206525454',
                'allows_multiple_answers': False, 'total_voter_count': 0, 'is_anonymous': False,
                'options': [{'voter_count': 0, 'text': '사요'}, {'voter_count': 0, 'text': '사지 마요'}],
                'is_closed': False,
                'question': 'decentralland 토큰 아이디 11579208923731619542357098500868790782672796004580736388931436462823 '
                            'NFT 9.58%만큼 저평가돼 있습니다. NFT bank의 가치 추정치는 5197 ETH이고, 현재 매도 호가는 4699.0 ETH입니다.한편, DAO 공동계좌가 보유하고 있는 잔여 ETH는 10000입니다.구매 여부를 투표해주세요.',
                'close_date': None},
       'all_members_are_administrators': True,
       'message_id': 139,
       'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 'photo': [],
       'entities': [], 'new_chat_members': [], 'new_chat_photo': [], 'caption_entities': [],
       'from': {'username': 'NFTscannerbot', 'id': 1934759690, 'first_name': 'NFTscanner', 'is_bot': True}}

# from telegram import Bot
#
# token = '1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8'
#
# bot = Bot(token=token)
# bot.delete_message(chat_id='-443191914', message_id=139)

qqq = {'update_id': 861595762,
       'poll_answer':
           {'poll_id': '6084757438999822359',
            'user': {'id': 1743100030, 'is_bot': False, 'first_name': 'Changwoo', 'last_name': 'Nam',
                     'username': 'vandlaw'},
            'option_ids': [0]}}

# requests.post('http://127.0.0.1:5000/', json=qqq)


local_url = "http://127.0.0.1:5000/"
real_url = "https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8"


class SellPollTest(unittest.TestCase):
    chat_id = ""
    user_id_a = ""
    user_id_b = ""
    webhook_endpoint = ""
    poll_id = 0
    token_id = ""

    def setUp(self):
        self.chat_id = "-443191914"
        self.user_id_a = "1743100030"
        self.user_id_b = "1805564465"
        self.token_id = "eeee"
        self.webhook_endpoint = real_url

        gov_dist = db.collection('dao').document(self.chat_id).collection('gov_distribution').document(
            'distribution').get().to_dict()
        gov_values = db.collection('dao').document(self.chat_id).collection('gov_values').document(
            'values').get().to_dict()
        quorum = gov_values['gov_token_total'] * gov_values['consent_limit'] / 100
        self.assertGreaterEqual(gov_dist[self.user_id_a] + gov_dist[self.user_id_b], quorum)

    def test_total(self):
        def add_holding_list(self):
            holding_data = {
                'project': "decentralland",
                'project_address': "aaa",
                'chain': "ethereum",
                "token_id": self.token_id,
                'category': "parcel",
                'price_buy': 1000,
                'price_est': 1300,
                'price_high': 2500,
                'on_sale': False
            }
            db.collection('dao').document(self.chat_id).collection('nft_holdings').add(holding_data)

        def make_sell_poll(self):
            selling_data = {
                'project': "decentralland",
                'project_address': "aaa",
                'chain': "ethereum",
                "token_id": self.token_id,
                'category': "parcel",
                'price_buy': 1000,
                'price_est': 1300,
                'is_buy_poll': False,
                'consent_token_amount': 0,
                'quorum': 12000 * (1 / 2),
                'consent_list': [],
                'reject_list': [],
                'price_high': 2500
            }

            updater = Updater(token=token)
            dispatcher = updater.dispatcher

            self.poll_id = start_telegram_poll(updater, dispatcher, selling_data, self.chat_id)

            del selling_data['price_high']
            selling_data['poll_id'] = self.poll_id
            db.collection('dao').document(self.chat_id).collection('nft_pendings').add(selling_data)
            db.collection('global').document('global').update(
                {'poll_list': firestore.ArrayUnion([self.poll_id])})
            db.collection('global').document('poll_index').update({str(self.poll_id): self.chat_id})

        def send_poll_answers(self):
            answer_data_a = {
                'update_id': 1,
                'poll_answer':
                    {'poll_id': self.poll_id,
                     'user': {'id': self.user_id_a, 'is_bot': False, 'first_name': 'Changwoo', 'last_name': 'Nam',
                              'username': 'vandlaw'},
                     'option_ids': [0]}}

            answer_data_b = {
                'update_id': 1,
                'poll_answer':
                    {'poll_id': self.poll_id,
                     'user': {'id': self.user_id_a, 'is_bot': False, 'first_name': 'aa', 'last_name': 'bb',
                              'username': 'cc'},
                     'option_ids': [0]}}
            log = logging.getLogger("TestLog")
            response1 = requests.post(self.webhook_endpoint, json=answer_data_a).json()
            log.debug(response1)
            response2 = requests.post(self.webhook_endpoint, json=answer_data_b).json()
            log.debug(response2)

            nft_in_poll = db.collection('dao').document(self.chat_id).collection('nft_holdings') \
                .where('token_id', '==', self.token_id).get()[0].to_dict()
            self.assertTrue(nft_in_poll["on_sale"])

        add_holding_list(self)
        make_sell_poll(self)
        # send_poll_answers(self)


class BuyTest(unittest.TestCase):
    chat_id = ""
    user_id_a = ""
    user_id_b = ""
    webhook_endpoint = ""
    poll_id = 0
    token_id = ""
    price_buy = 0
    price_est = 0
    quorum = 0

    def setUp(self):
        self.chat_id = "-443191914"
        self.user_id_a = "1743100030"  # 남창우
        self.user_id_b = "1805564465"  # 정수현
        self.token_id = "xxxxxxxx"
        self.price_buy = 1500
        self.price_est = 2000
        self.webhook_endpoint = local_url

        gov_dist = db.collection('dao').document(self.chat_id).collection('gov_distribution').document(
            'distribution').get().to_dict()
        gov_values = db.collection('dao').document(self.chat_id).collection('gov_values').document(
            'values').get().to_dict()
        self.quorum = gov_values['gov_token_total'] * gov_values['consent_limit'] / 100
        self.assertGreaterEqual(gov_dist[self.user_id_a] + gov_dist[self.user_id_b], self.quorum)

    def test_buy(self):
        def make_poll(self):
            data = {
                'project': 'decentralland',
                'project_address': 'aaa',
                'chain': 'ethereum',
                'token_id': self.token_id,
                'category': "parcel",
                'price_buy': self.price_buy,
                'price_est': self.price_est,
                'consent_token_amount': 0,
                'is_buy_poll': True,
                'consent_list': [],
                'reject_list': [],
                'quorum': self.quorum
            }

            updater = Updater(token=token)
            dispatcher = updater.dispatcher
            self.poll_id = start_telegram_poll(updater, dispatcher, data, self.chat_id)
            data["poll_id"] = self.poll_id

            db.collection('dao').document(self.chat_id).collection('nft_pendings').add(data)
            db.collection('global').document('global').update(
                {'poll_list': firestore.ArrayUnion([self.poll_id])})
            db.collection('global').document('poll_index').update({str(self.poll_id): self.chat_id})

        def send_answer(self):
            answer_data_a = {
                'update_id': 1,
                'poll_answer':
                    {'poll_id': self.poll_id,
                     'user': {'id': self.user_id_a, 'is_bot': False, 'first_name': 'Changwoo', 'last_name': 'Nam',
                              'username': 'vandlaw'},
                     'option_ids': [0]}}

            answer_data_b = {
                'update_id': 1,
                'poll_answer':
                    {'poll_id': self.poll_id,
                     'user': {'id': self.user_id_b, 'is_bot': False, 'first_name': 'aa', 'last_name': 'bb',
                              'username': 'cc'},
                     'option_ids': [0]}}
            log = logging.getLogger("TestLog")
            response1 = requests.post(self.webhook_endpoint, json=answer_data_a).json()
            log.debug(response1)
            response2 = requests.post(self.webhook_endpoint, json=answer_data_b).json()
            log.debug(response2)
            nft_in_holdings = db.collection('dao').document(self.chat_id).collection('nft_holdings') \
                .where('token_id', '==', self.token_id).get()
            self.assertTrue(len(nft_in_holdings) > 0)
            nft_in_pendings = db.collection('dao').document(self.chat_id).collection('nft_pendings') \
                .where('token_id', '==', self.token_id).get()
            self.assertTrue(len(nft_in_pendings) == 0)
            nft_in_transactions = db.collection('dao').document(self.chat_id).collection('nft_transactions') \
                .where('token_id', '==', self.token_id).get()
            self.assertTrue(len(nft_in_transactions) > 0)

        make_poll(self)
        send_answer(self)


dao_start = {'chat_room_id': -12345,
             'eth_address': 'aaaaaaaa',
             'gov_distribution': {'1': 3000, '2': 4000, '3': 3000},
             'gov_values': {'underrating_ratio': 10, 'consent_limit': 50,
                            'price_collapse_ratio': 30, 'index_weight': 50,
                            'gov_token_total': 10000}
             }


dao_start2 = {'chat_room_id': -98765,
              'eth_account': 'bbbbbb',
              'gov_distribution': {'1': 3000, '2': 4000, '3': 3000},
              'gov_values': {'underrating_ratio': 10, 'buy_limit_ratio': 50,
                             'price_collapse_ratio': 30, 'index_weight': 50,
                             'gov_token_total': 12000, 'consent_limit': 50}
              }

dao_update = {'chat_room_id': -12345,
              # 'gov_distribution': {'1': 3000, '2': 4000, '3': 3000},
              'gov_values': {'underrating_ratio': 30, 'consent_limit': 55}
              }

if __name__ == '__main__':
    # logging.basicConfig(stream=sys.stderr)
    # logging.getLogger("TestLog").setLevel(logging.DEBUG)
    # unittest.main()
    webhook_endpoint = 'http://localhost:5000/daoDetail/'
    response = requests.post(webhook_endpoint, json={'chat_room_id': "-443191914"}).json()
    print(response)
