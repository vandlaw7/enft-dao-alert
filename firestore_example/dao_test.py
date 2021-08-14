import firebase_admin
import requests
from firebase_admin import credentials, firestore

import datetime

from telegram.ext import Updater

cred = credentials.Certificate("../enft-price-check/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

chat_room_id = 123456789

data_send = {'name': 'John Smith', 'age': 42, 'employed': False}
data_two = {'category': 'parcel', 'chain': 'ethereum'}
# db.collection(chat_room_id).document('public_account').set(data_send)
# db.collection(chat_room_id).document('nft_pendings').collections('123').set('data_two')

# db.collection('dao').document(str(chat_room_id)).set(data_send)
# db.collection('dao').document(chat_room_id).collection('nft_pendings').add(data_two)

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

dao_start = {'chat_room_id': -12345,
             'eth_address': 'aaaaaaaa',
             'gov_distribution': {'1': 3000, '2': 4000, '3': 3000},
             'gov_values': {'underrating_ratio': 10, 'consent_limit': 50,
                            'price_collapse_ratio': 30, 'index_weight': 50,
                            'gov_token_total': 10000}
             }

dao_start2 = {'chat_room_id': 98765,
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

requests.post('http://127.0.0.1:5000/', json=qqq)


def test_sell_poll():
    holding_data = {
        'project': "decentralland",
        'project_address': "aaa",
        'chain': "ethereum",
        "token_id": "11111111",
        'category': "parcel",
        'price_buy': 1000,
        'price_est': 1300,
        'on_sale': False
    }
    db.collection('dao').document(chat_room_id).collection('nft_holdings').add(holding_data)

