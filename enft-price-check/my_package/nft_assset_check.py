import requests
import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import time

from my_package.polling_bot import start_telegram_poll, start_fake_poll
from my_package.global_var import total_gov_token, db


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
    print(result)

    # 투표 체크용 가짜
    start_fake_poll(updater, dispatcher)

    for i in range(len(result['orders'])):
        print(f'{i}번째 매물')
        token_id_deland = result['orders'][i]['tokenId']
        category = result['orders'][i]['category']
        price_check_url = f'https://api.nftbank.ai/estimates-v2/estimates/{decentral_land_contract_id}/{token_id_deland}?chain_id=ETHEREUM'
        r3 = requests.get(price_check_url, headers=headers)
        estimated_result = json.loads(r3.text)
        if len(estimated_result['data']) != 0:
            nft_bank_estimate = int(estimated_result['data'][0]['estimate'][0]['estimate_price'])
            now_price = int(result['orders'][i]['price']) / pow(10, 18)
            if nft_bank_estimate > now_price * 1.1:
                print("당장 사요!")
                data = {
                    'project': 'decentralland',
                    'project_address': decentral_land_contract_id,
                    'chain': 'ethereum',
                    'token_id': token_id_deland,
                    'category': category,
                    'price_buy': now_price,
                    'price_est': nft_bank_estimate,
                    'consent_token_amount': 0,
                    'is_buy_poll': True,
                    'quorum': total_gov_token * (1 / 2),
                    'consent_list': [],
                    'reject_list': []
                }

                poll_id = start_telegram_poll(updater, dispatcher, data)

                data['poll_id'] = poll_id
                db.collection('nft_pendings').add(data)
