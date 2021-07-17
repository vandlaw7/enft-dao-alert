from telegram.ext import Updater

from my_package.polling_bot import token
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

    updater.start_polling()

    check_prices(updater, dispatcher)

    # to fix telegram bug, which is frequently reset the webhook address
    requests.get(
        'https://api.telegram.org/bot1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8/setWebhook?url=https://us-central1-enft-project.cloudfunctions.net/pollHandle')

    return OK_RESPONSE


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def pollHandle_flask():
    """ Runs the Telegram webhook """

    ''' below is request.data example form telegram poll answer
    {'update_id': 861595762, 
    'poll_answer': 
    {'poll_id': '6310048449567916050', 
    'user': {'id': 1743100030, 'is_bot': False, 'first_name': 'Changwoo', 'last_name': 'Nam', 'username': 'vandlaw'}, 
    'option_ids': [1]}}'''

    chat_dict = json.loads(request.data)['poll_answer']

    poll_id = chat_dict['poll_id']
    telegram_id = chat_dict['user']['id']
    nft_in_poll = db.collection('nft_pendings').where('poll_id', '==', poll_id).get()
    nft_dict = nft_in_poll.to_dict()

    # 0 means 'consent'
    consent = (chat_dict['option_ids'][0] == 0)

    if len(nft_in_poll) == 0:
        return ERROR_RESPONSE

    user_doc = db.collection('members').where('telegram_id', '==', telegram_id)
    gov_token = user_doc.to_dict()['gov_token']

    if consent:
        db.collection('nft_pendings').document(nft_in_poll.id).update(
            {'consent_list': firestore.ArrayUnion([telegram_id]),
             'consent_token_amount': firestore.Increment(gov_token)})

        if nft_dict['consent_token_amount'] >= nft_dict['quorum']:

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
                if not db.collection('public_account').document('public').to_dict()['eth_remain'] >= nft_dict['price_buy']:
                    return ERROR_RESPONSE

                ''' NFT buying web3 solidity code (@Daniel)'''

                ''' pending list out, holding/transaction list in '''
                data_holding_unique = {'on_sale': False}
                data_transaction_unique = {
                    'price_sell': 0,
                    'date_buy': datetime.date.today(),
                    'data_sell': datetime.date(2100, 12, 31)
                }

                data_holding = data_intersection.copy()
                data_holding.update(data_holding_unique)
                data_transaction = data_intersection.copy()
                data_transaction.update(data_transaction_unique)

                db.collection('nft_holdings').add(data_holding)
                db.collection('nft_transactions').add(data_transaction)
                db.collection('nft_pendings').document(nft_in_poll.id).delete()
            else:
                ''' NFT selling web3 solidity code (@Daniel)'''

                ''' if selling is done, we have to update DB. '''


    else:
        db.collection('nft_pendings').document(nft_in_poll.id).update(
            {'buy_reject_list': firestore.ArrayUnion([telegram_id])})

    return OK_RESPONSE


def pollHandle_flask(request):
    """ Runs the Telegram webhook """

    ''' below is request.data example form telegram poll answer
    {'update_id': 861595762, 
    'poll_answer': 
    {'poll_id': '6310048449567916050', 
    'user': {'id': 1743100030, 'is_bot': False, 'first_name': 'Changwoo', 'last_name': 'Nam', 'username': 'vandlaw'}, 
    'option_ids': [1]}}'''

    chat_dict = json.loads(request.data)['poll_answer']

    poll_id = chat_dict['poll_id']
    telegram_id = chat_dict['user']['id']
    nft_in_poll = db.collection('nft_pendings').where('poll_id', '==', poll_id).get()
    nft_dict = nft_in_poll.to_dict()

    # 0 means 'consent'
    consent = (chat_dict['option_ids'][0] == 0)

    if len(nft_in_poll) == 0:
        return ERROR_RESPONSE

    user_doc = db.collection('members').where('telegram_id', '==', telegram_id)
    gov_token = user_doc.to_dict()['gov_token']

    if consent:
        db.collection('nft_pendings').document(nft_in_poll.id).update(
            {'consent_list': firestore.ArrayUnion([telegram_id]),
             'consent_token_amount': firestore.Increment(gov_token)})

        if nft_dict['consent_token_amount'] >= nft_dict['quorum']:

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
                if not db.collection('public_account').document('public').to_dict()['eth_remain'] >= nft_dict['price_buy']:
                    return ERROR_RESPONSE

                ''' NFT buying web3 solidity code (@Daniel)'''

                ''' pending list out, holding/transaction list in '''
                data_holding_unique = {'on_sale': False}
                data_transaction_unique = {
                    'price_sell': 0,
                    'date_buy': datetime.date.today(),
                    'data_sell': datetime.date(2100, 12, 31)
                }

                data_holding = data_intersection.copy()
                data_holding.update(data_holding_unique)
                data_transaction = data_intersection.copy()
                data_transaction.update(data_transaction_unique)

                db.collection('nft_holdings').add(data_holding)
                db.collection('nft_transactions').add(data_transaction)
                db.collection('nft_pendings').document(nft_in_poll.id).delete()
            else:
                ''' NFT selling web3 solidity code (@Daniel)'''

                ''' if selling is done, we have to update DB. '''


    else:
        db.collection('nft_pendings').document(nft_in_poll.id).update(
            {'buy_reject_list': firestore.ArrayUnion([telegram_id])})

    return OK_RESPONSE


if __name__ == '__main__':
    app.run()
