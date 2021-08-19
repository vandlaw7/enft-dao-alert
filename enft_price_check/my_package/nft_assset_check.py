import json
import time

import requests
from firebase_admin import firestore
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from my_package.global_var import db
from my_package.polling_bot import start_telegram_poll

url = "https://api.nftbank.ai/estimates-v2/dapp/decentraland"
headers = {'x-api-key': 'b8bb9504e550e732265f08434414b8dd'}

# Select your transport with a defined url endpoint
transport = RequestsHTTPTransport(url="https://api.thegraph.com/subgraphs/name/decentraland/marketplace")
# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

decentral_land_contract_id = '0xf87e31492faf9a91b02ee0deaad50d51d56d5d4d'

current_time = time.time()
yesterday_time = int(current_time - 24 * 60 * 60)
how_many = 100
decentral_land_string = f'''
{{
orders (first: {how_many} 
    orderBy: updatedAt, 
    orderDirection: desc 
    where: {{ 
        status: open
        updatedAt_gt:{yesterday_time}}}
) 
  {{
    category
    price
    updatedAt
    tokenId
 }}
}}
'''


def get_query(my_string):
    query = gql(my_string)
    result = client.execute(query)
    return result


def check_prices(updater, dispatcher):
    query = gql(decentral_land_string)
    result = client.execute(query)

    only_one = True

    for i in range(len(result['orders'])):
        print(f'{i}번째 매물')
        token_id = result['orders'][i]['tokenId']
        category = result['orders'][i]['category']
        price_check_url = f'https://api.nftbank.ai/estimates-v2/estimates/' \
                          f'{decentral_land_contract_id}/{token_id}?chain_id=ETHEREUM'
        r3 = requests.get(price_check_url, headers=headers)
        estimated_result = json.loads(r3.text)
        if estimated_result['data']:
            nft_bank_estimate = int(estimated_result['data'][0]['estimate'][0]['estimate_price'])
            now_price = int(result['orders'][i]['price']) / pow(10, 18)
            print(nft_bank_estimate)
            print(now_price)

            data = {
                'project': 'decentralland',
                'project_address': decentral_land_contract_id,
                'chain': 'ethereum',
                'token_id': token_id,
                'category': category,
                'price_buy': now_price,
                'price_est': nft_bank_estimate,
                'consent_token_amount': 0,
                'is_buy_poll': True,
                'consent_list': [],
                'reject_list': []
            }

            # if only_one:
            #     only_one = False
            #     chat_ids = db.collection('global').document('global').get().to_dict()["chat_list"]
            #     print(chat_ids)
            #     for chat_id in chat_ids:
            #         dao_governance = db.collection('dao').document(str(chat_id)).collection('gov_values').document(
            #             'values').get().to_dict()
            #         data['quorum'] = dao_governance['gov_token_total'] * dao_governance['consent_limit'] / 100
            #         poll_id = start_telegram_poll(updater, dispatcher, data, chat_id)
            #         data['poll_id'] = poll_id
            #         db.collection('dao').document(str(chat_id)).collection('nft_pendings').add(data)
            #         db.collection('global').document('global').update({'poll_list': firestore.ArrayUnion([poll_id])})

            if nft_bank_estimate > now_price:
                chat_ids = db.collection('global').document('global').get().to_dict()["chat_list"]
                for chat_id in chat_ids:

                    if db.collection('dao').document(str(chat_id)).collection('nft_pendings').where('token_id', '==',
                                                                                                 token_id).get():
                        print("이미 pending list에 있는 NFT입니다.")
                        continue

                    dao_governance = db.collection('dao').document(str(chat_id)).collection('gov_values').document(
                        'values').get().to_dict()
                    underrating_ratio = dao_governance['underrating_ratio']

                    if nft_bank_estimate - now_price >= nft_bank_estimate * underrating_ratio / 100:
                        print(chat_id, "당장 사요!")
                        data['quorum'] = dao_governance['gov_token_total'] * dao_governance['consent_limit'] / 100
                        poll_id = start_telegram_poll(updater, dispatcher, data, chat_id)
                        data['poll_id'] = poll_id
                        db.collection('dao').document(str(chat_id)).collection('nft_pendings').add(data)
                        db.collection('global').document('global').update(
                            {'poll_list': firestore.ArrayUnion([poll_id])})
                        db.collection('global').document('poll_index').update({str(poll_id): chat_id})
