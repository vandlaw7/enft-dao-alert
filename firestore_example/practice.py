import firebase_admin
import requests
from firebase_admin import credentials, firestore

cred = credentials.Certificate("../enft-price-check/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

chat_room_id = 123456789

data_send = {'name': 'John Smith', 'age': 42, 'employed': False}
data_two = {'category': 'parcel', 'chain': 'ethereum'}
# db.collection(chat_room_id).document('public_account').set(data_send)
# db.collection(chat_room_id).document('nft_pendings').collections('123').set('data_two')

db.collection('dao').document(str(chat_room_id)).set(data_send)
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

dao_start = {'chat_room_id': -557391640,
             'eth_account': 'aaaaaaaa',
             'gov_distribution': {'1': 3000, '2': 4000, '3': 3000},
             'gov_values': {'underrating_ratio': 10, 'buy_limit_ratio': 50,
                            'price_collapse_ratio': 30, 'index_weight': 50}
             }

dao_start2 = {'chat_room_id': 98765,
             'eth_account': 'bbbbbb',
             'gov_distribution': {'1': 3000, '2': 4000, '3': 3000},
             'gov_values': {'underrating_ratio': 10, 'buy_limit_ratio': 50,
                            'price_collapse_ratio': 30, 'index_weight': 50,
                            'gov_token_total': 12000, 'consent_limit': 50}
             }

dao_update = {'chat_room_id': -557391640,
              'eth_account': 'aaaaaaaa',
              'gov_distribution': {'1': 3000, '2': 4000, '3': 5000},
             'gov_values': {'underrating_ratio': 10, 'buy_limit_ratio': 50,
                            'price_collapse_ratio': 30, 'index_weight': 50,
                            'gov_token_total': 12000, 'consent_limit': 50}
             }

# requests.post('http://127.0.0.1:5000/daoSetting/', json=dao_start2)
