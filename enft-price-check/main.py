from telegram.ext import Updater

from my_package.nft_holdings_update import update_est_prices
from my_package.polling_bot import token, nft_scanner_id
from my_package.nft_assset_check import check_prices

import json
import logging
import requests
import datetime

from my_package.global_var import db

from firebase_admin import firestore

from flask import Flask, request

logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

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
    # now for debug
    # update_est_prices(updater, dispatcher)

    # to fix telegram bug, which frequently resets the webhook address
    requests.get(
        'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/setWebhook?url=https://us-central1-enft-project.cloudfunctions.net/pollHandle')

    return OK_RESPONSE


app = Flask(__name__)


def enftAlert_local():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    check_prices(updater, dispatcher)
    # now for debug
    # update_est_prices(updater, dispatcher)

    # to fix telegram bug, which frequently resets the webhook address
    # drop_pending_updates=True option is for handling infinite request errors.
    requests.get(
        'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/setWebhook'
        '?url=https://us-central1-enft-project.cloudfunctions.net/pollHandle'
        '&drop_pending_updates=True')

    return OK_RESPONSE


@app.route('/', methods=['GET', 'POST'])
def pollHandle():
    """ Runs the Telegram webhook """

    data = json.loads(request.data)
    print(data)

    if not 'poll_answer' in data:
        return OK_RESPONSE

    ''' below is request.data example form telegram poll answer
       {'update_id': 861595762, 
       'poll_answer': 
       {'poll_id': '6310048449567916050', 
       'user': {'id': 1743100030, 'is_bot': False, 'first_name': 'Changwoo', 'last_name': 'Nam', 'username': 'vandlaw'}, 
       'option_ids': [1]}}'''

    chat_dict = json.loads(request.data)['poll_answer']

    poll_id = str(chat_dict['poll_id'])
    telegram_id = str(chat_dict['user']['id'])
    dao_id = db.collection('global').document('poll_index').get().to_dict()[poll_id]

    nft_in_poll = db.collection('dao').document(dao_id).collection('nft_pendings') \
        .where('poll_id', '==', poll_id).get()[0]
    nft_dict = nft_in_poll.to_dict()

    # 0 means 'consent'
    consent = (chat_dict['option_ids'][0] == 0)

    gov_distribution = db.collection('dao').document(dao_id).collection('gov_distribution').document(
        'distribution').get().to_dict()
    print("gov_distribution")
    print(gov_distribution)
    gov_token = gov_distribution[telegram_id]

    if consent:
        db.collection('dao').document(dao_id).collection('nft_pendings').document(nft_in_poll.id).update(
            {'consent_list': firestore.ArrayUnion([telegram_id]),
             'consent_token_amount': firestore.Increment(gov_token)})

        print("구입 조건 판별")
        print(nft_dict['quorum'])
        print(nft_dict['consent_token_amount'])
        print(gov_token)

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
                data_holding_unique = {'on_sale': False}
                data_transaction_unique = {
                    'price_sell': None,
                    'date_buy': datetime.datetime.now(),
                    'data_sell': None
                }

                data_holding = data_intersection.copy()
                data_holding.update(data_holding_unique)
                data_transaction = data_intersection.copy()
                data_transaction.update(data_transaction_unique)

                db.collection('dao').document(dao_id).collection('nft_holdings').document().set(data_holding)
                db.collection('dao').document(dao_id).collection('nft_transactions').document().set(data_transaction)
                db.collection('dao').document(dao_id).collection('nft_pendings').document(nft_in_poll.id).delete()
            else:
                ''' NFT selling web3 solidity code (@Daniel)'''

                ''' if selling is done, we have to update DB. '''


    else:
        db.collection('nft_pendings').document(nft_in_poll.id).update(
            {'buy_reject_list': firestore.ArrayUnion([telegram_id])})

    return OK_RESPONSE


@app.route('/daoSetting/', methods=['GET', 'POST'])
def daoSetting():
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
        db.collection('dao').document(chat_room_id).set({'eth_address': eth_address})
        db.collection('global').document('global').update({'chat_list': firestore.ArrayUnion([chat_room_id])})
        db.collection('dao').document(chat_room_id).collection('gov_distribution').document('distribution').set(
            gov_distribution)
        db.collection('dao').document(chat_room_id).collection('gov_values').document('values').set(gov_values)
    # update mode
    else:
        if gov_distribution is not None:
            db.collection('dao').document(chat_room_id).collection('gov_distribution').document('distribution').update(
                gov_distribution)
        if gov_values is not None:
            db.collection('dao').document(chat_room_id).collection('gov_values').document('values').update(gov_values)

    return OK_RESPONSE


if __name__ == '__main__':
    # enftAlert_local()
    app.run()
