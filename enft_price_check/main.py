import datetime
import json
import logging

import requests
from firebase_admin import firestore
from flask import Flask, request
import flask
from telegram.ext import Updater

from my_package.global_var import db
from my_package.nft_assset_check import check_prices
from my_package.nft_holdings_update import update_price_estimations
from my_package.polling_bot import token

from flask_cors import CORS

# logger = logging.getLogger()
# if logger.handlers:
#     for handler in logger.handlers:
#         logger.removeHandler(handler)
# logging.basicConfig(level=logging.INFO)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('Oops, something went wrong!')
}


def enftAlert(request):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    check_prices(updater, dispatcher)
    update_price_estimations(updater, dispatcher)

    # to fix telegram bug, which frequently resets the webhook address
    requests.get(
        'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/setWebhook'
        '?url=https://us-central1-enft-project.cloudfunctions.net/pollHandle'
        '&drop_pending_updates=True')

    return OK_RESPONSE


# def enftAlert_local():
#     updater = Updater(token=token)
#     dispatcher = updater.dispatcher

#     check_prices(updater, dispatcher)
#     update_price_estimations(updater, dispatcher)

#     # to fix telegram bug, which frequently resets the webhook address
#     # drop_pending_updates=True option is for handling infinite request errors.
#     requests.get(
#         'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/setWebhook'
#         '?url=https://us-central1-enft-project.cloudfunctions.net/pollHandle'
#         '&drop_pending_updates=True')

#     return OK_RESPONSE


app = Flask("internal")
CORS(app)


# @app.route('/', methods=['GET', 'POST'])
def pollHandle(request):
    """ Runs the Telegram webhook """

    data = json.loads(request.data)
    print(data)

    if 'message' in data:
        message_dict = data['message']
        chat_id = message_dict["chat"]["id"]
        if message_dict["text"] == '/chatid':
            sending_message = f'Chat id of this group chat is {chat_id}. Chat id must have minus sign.'
            requests.get(
                f'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/sendMessage'
                f'?chat_id={chat_id}&text={sending_message}')
        elif message_dict["text"] == '/userid':
            user_id = message_dict["from"]["id"]
            sending_message = f'Your telegram user_id is {user_id}'
            requests.get(
                f'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/sendMessage'
                f'?chat_id={chat_id}&text={sending_message}')

        return OK_RESPONSE

    if 'poll_answer' not in data:
        print("투표 응답이 아님")
        return OK_RESPONSE

    ''' Below is request.data example form telegram poll answer
       {'update_id': 861595762, 
       'poll_answer': {'poll_id': '6310048449567916050', 
                       'user': {'id': 1743100030, 'is_bot': False, 'first_name': 'Changwoo', 'last_name': 'Nam', 'username': 'vandlaw'}, 
                       'option_ids': [1]}}'''

    chat_dict = data['poll_answer']
    if not chat_dict['option_ids']:
        print("투표 취소")
        return OK_RESPONSE

    poll_id = str(chat_dict['poll_id'])
    telegram_id = str(chat_dict['user']['id'])
    dao_id = db.collection('global').document(
        'poll_index').get().to_dict().get(poll_id)
    if dao_id:
        nft_in_poll_raw = db.collection('dao').document(dao_id).collection('nft_pendings').where('poll_id', '==',
                                                                                                 poll_id).get()
        if nft_in_poll_raw:
            nft_in_poll = nft_in_poll_raw[0]
            nft_dict = nft_in_poll.to_dict()
        else:
            sending_message = f"This NFT is not enrolled in this DAO's poll list."
            requests.get(
                f'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/sendMessage'
                f'?chat_id={dao_id}&text={sending_message}')
            return OK_RESPONSE

    else:
        print("이미 팔려서 리스트에서 지워진 NFT입니다.")
        ''' 여기에 텔레그램 챗으로 안내를 할 지 여부 좀 생각해봐야 함.'''
        return OK_RESPONSE

    # 0 means 'consent'
    consent = (chat_dict['option_ids'][0] == 0)

    gov_distribution = db.collection('dao').document(dao_id).collection('gov_distribution').document(
        'distribution').get().to_dict()
    gov_token = gov_distribution.get(telegram_id)
    if not gov_token:
        print("DAO에 등록되지 않은 사용자입니다.")
        sending_message = f'telegram id {telegram_id} user is not enrolled in DAO. This answer is invalidate.'
        requests.get(
            f'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/sendMessage'
            f'?chat_id={dao_id}&text={sending_message}')
        return OK_RESPONSE

    if consent:
        db.collection('dao').document(dao_id).collection('nft_pendings').document(nft_in_poll.id).update(
            {'consent_list': firestore.ArrayUnion([telegram_id]),
             'consent_token_amount': firestore.Increment(gov_token)})

        if nft_dict['consent_token_amount'] + gov_token >= nft_dict['quorum']:
            print("조건 통과함!")
            data_intersection = {
                'project': nft_dict['project'],
                'project_address': nft_dict['project_address'],
                'chain': nft_dict['chain'],
                'token_id': nft_dict['token_id'],
                'category': nft_dict['category'],
                'price_buy': nft_dict['price_buy'],
                'price_est': nft_dict['price_est'],
            }

            if nft_dict['is_buy_poll']:
                print("구입 진행!")
                if not db.collection('dao').document(dao_id).get().to_dict()['eth_remain'] >= nft_dict['price_buy']:
                    return ERROR_RESPONSE

                ''' NFT buying web3 solidity code (@Daniel)'''

                ''' pending list out, holding/transaction list in '''
                data_holding_unique = {
                    'on_sale': False,
                    'price_high': nft_dict['price_buy']
                }
                data_transaction_unique = {
                    'price_sell': None,
                    'date_buy': datetime.datetime.now(),
                    'date_sell': None
                }

                data_holding = data_intersection.copy()
                data_holding.update(data_holding_unique)
                data_transaction = data_intersection.copy()
                data_transaction.update(data_transaction_unique)

                db.collection('dao').document(dao_id).collection(
                    'nft_holdings').document().set(data_holding)
                db.collection('dao').document(dao_id).collection(
                    'nft_transactions').document().set(data_transaction)
                db.collection('dao').document(dao_id).collection(
                    'nft_pendings').document(nft_in_poll.id).delete()

                db.collection('dao').document(dao_id).update(
                    {'eth_remain': firestore.Increment(-1 * nft_dict['price_buy'])})
                # db.collection('persons').document('p1').update({'age': firestore.Increment(10)})

                sending_message = f'decentralland token ID {nft_dict["token_id"]} 구매에 성공하였습니다!'
                requests.get(
                    f'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/sendMessage'
                    f'?chat_id={dao_id}&text={sending_message}')

                # 다른 DAO에게 이제 이 NFT를 구입할 수 없게 되었다는 것을 알리고, 우리 서비스 DB도 수정해준다.
                db.collection('global').document('poll_index').update(
                    {poll_id: firestore.DELETE_FIELD})
                chat_ids = db.collection('global').document(
                    'global').get().to_dict()["chat_list"]

                for chat_id in chat_ids:
                    nft_sold = db.collection('dao').document(chat_id).collection('nft_pendings') \
                        .where("token_id", '==', nft_dict['token_id']).get()

                    # 어차피 하나지만 firestore where 문법의 특성상 list 형태로 리턴되므로 그냥 이런 형식을 취해준다.
                    # list가 없으면 그냥 지나칠 때니 여러모로 편하다.
                    for nft in nft_sold:
                        if nft.to_dict()["project"] == nft_dict['project']:
                            key = nft.id
                            db.collection('dao').document(chat_id).collection(
                                'nft_pendings').document(key).delete()

                            sending_message = f'{data_intersection["project"]} token id {data_intersection["token_id"]} ' \
                                              f'NFT is sold by other user. Polling about  '
                            requests.get(
                                f'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/sendMessage'
                                f'?chat_id={chat_id}&text={sending_message}')

                            print("NFT 구매가 완료되어, 다른 DAO들은 이 NFT를 구매할 수 없습니다.")
            else:
                ''' NFT selling web3 solidity code (@Daniel)'''

                nft_selling = db.collection('dao').document(dao_id).collection('nft_holdings') \
                    .where("token_id", '==', nft_dict['token_id']).get()
                for nft in nft_selling:
                    if nft.to_dict()["project"] == nft_dict['project']:
                        key = nft.id
                        db.collection('dao').document(dao_id).collection('nft_holdings').document(key).update(
                            {'on_sale': True})

                ''' if selling is done, we have to update DB. '''

    else:
        db.collection('dao').document(dao_id).collection('nft_pendings').document(nft_in_poll.id).update(
            {'buy_reject_list': firestore.ArrayUnion([telegram_id])})

    # drop_pending_updates=True option is for handling infinite request errors.
    requests.get(
        'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/setWebhook'
        '?url=https://us-central1-enft-project.cloudfunctions.net/pollHandle'
        '&drop_pending_updates=True')

    return OK_RESPONSE


# @app.route('/daoSetting/', methods=['GET', 'POST'])
def daoSetting(request):
    '''
    below is input data example
    chat_room_id must have minus value. (telegram naming rule)
    dao_start = {'chat_room_id': -12345,
             'eth_address': 'aaaaaaaa',
             'gov_distribution': {'1': 3000, '2': 4000, '3': 3000},
             'gov_values': {'underrating_ratio': 10, 'consent_limit': 50,
                            'price_collapse_ratio': 30, 'index_weight': 50}
             }
    '''
    data = json.loads(request.data)
    chat_room_id, eth_address, gov_distribution, gov_values = str(data.get("chat_room_id")), data.get(
        "eth_address"), data.get('gov_distribution'), data.get('gov_values')

    # create mode
    if not db.collection('dao').document(chat_room_id).get().exists:

        db.collection('dao').document(chat_room_id).set(
            {'eth_address': eth_address})
        db.collection('global').document('global').update(
            {'chat_list': firestore.ArrayUnion([chat_room_id])})
        db.collection('dao').document(chat_room_id).collection('gov_distribution').document('distribution').set(
            gov_distribution)
        db.collection('dao').document(chat_room_id).collection(
            'gov_values').document('values').set(gov_values)

    # update mode
    else:
        if gov_distribution is not None:
            db.collection('dao').document(chat_room_id).collection('gov_distribution').document('distribution').update(
                gov_distribution)
        if gov_values is not None:
            db.collection('dao').document(chat_room_id).collection(
                'gov_values').document('values').update(gov_values)

    return OK_RESPONSE

# Define the internal path, idiomatic Flask definition


@app.route('/user/<string:id>', methods=['GET', 'POST'])
def users(id):
    print(id)
    return id, 200


@app.route('/dao/<string:id>/detail', methods=['GET', 'POST'])
def daoDetail(id):
    print(id)

    nft_holdings_collection = db.collection('dao').document(id)\
        .collection('nft_holdings').get()
    nft_holdings = {}

    gov_distribution = db.collection('dao').document(id)\
        .collection('gov_distribution').document('distribution')\
        .get().to_dict()

    gov_values = db.collection('dao').document(id)\
        .collection('gov_values').document('values')\
        .get().to_dict()

    estimated_value = 0
    invested_value = 0
    for nft in nft_holdings_collection:
        nft_dict = nft.to_dict()
        nft_holdings[nft.id] = nft_dict

        estimated_value += nft_dict['price_high']
        invested_value += nft_dict['price_buy']
    remained_balance = db.collection('dao').document(
        id).get().to_dict()['eth_remain']

    return {
        'estimated_value': estimated_value,
        'invested_value': invested_value,
        'remained_balance': remained_balance,
        'nft_holdings': nft_holdings,
        'gov_distribution': gov_distribution,
        'gov_values': gov_values
    }


# @app.route('/dao/<string:id>/detail/<string:nft_id>', methods=['GET', 'POST'])
# def daoNftHoldingDetail(id, nft_id):


def main(request):
    # Create a new app context for the internal app
    internal_ctx = app.test_request_context(path=request.full_path,
                                            method=request.method)

    # Copy main request data from original request
    # According to your context, parts can be missing. Adapt here!
    internal_ctx.request.data = request.data
    internal_ctx.request.headers = request.headers

    # Activate the context
    internal_ctx.push()
    # Dispatch the request to the internal app and get the result
    return_value = app.full_dispatch_request()
    # Offload the context
    internal_ctx.pop()

    # Return the result of the internal app routing and processing
    return return_value


if __name__ == '__main__':
    # enftAlert_local()
    app.run(debug=True)
