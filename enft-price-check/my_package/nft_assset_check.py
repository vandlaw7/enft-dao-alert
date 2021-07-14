import requests
import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import time

url = "https://api.nftbank.ai/estimates-v2/dapp/decentraland"
headers = {'x-api-key': 'b8bb9504e550e732265f08434414b8dd'}

# Select your transport with a defined url endpoint
transport = RequestsHTTPTransport(url="https://api.thegraph.com/subgraphs/name/decentraland/marketplace")
# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

current_time = time.time()
yesterday_time = int(current_time - 24 * 60 * 60)
how_many = 100
my_string = f'''
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


# print(my_string)
def get_query(my_string):
    query = gql(my_string)
    result = client.execute(query)
    return result

def check_prices(result):
    for i in range(len(result['orders'])):
        print(f'{i}번째 매물')
        token_id_deland = result['orders'][i]['tokenId']
        # print(token_id_deland)
        # print(int(result['orders'][i]['price']) / pow(10, 18))

        decentral_land_contract_id = '0xf87e31492faf9a91b02ee0deaad50d51d56d5d4d'
        price_check_url = f'https://api.nftbank.ai/estimates-v2/estimates/{decentral_land_contract_id}/{token_id_deland}?chain_id=ETHEREUM'
        r3 = requests.get(price_check_url, headers=headers)
        estimated_result = json.loads(r3.text)
        if len(estimated_result['data']) != 0:
            nft_bank_estimate = int(estimated_result['data'][0]['estimate'][0]['estimate_price'])
            # print('nft 뱅크 추정가')
            # print(nft_bank_estimate)
            now_price = int(result['orders'][i]['price']) / pow(10, 18)
            # print('매도 호가')
            # print(now_price)
            if nft_bank_estimate > now_price * 1.1:
                print("당장 사요!")
