import json
from gql.transport import requests
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# db Setup
cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# nft_bank api setup
nft_bank_api = 'b8bb9504e550e732265f08434414b8dd'
headers = {'x-api-key': nft_bank_api}


# update nft_holdings' estimates periodically
def update_est_prices():
    docs = db.collection('nft_holdings').get()
    for doc in docs:
        nft = doc.to_dict()
        price_check_url = f'https://api.nftbank.ai/estimates-v2/estimates/' \
                          f'{nft["project_address"]}/{nft["token_id"]}?chain_id={nft["chain"]}'
        r = requests.get(price_check_url, headers=headers)
        estimated_result = json.loads(r.text)
        nft_bank_est_value = float(estimated_result['data'][0]['estimate'][0]['estimate_price'])
        if nft_bank_est_value != float(nft["est_price"]):
            key = doc.id
            db.collection('nft_holdings').document(key).update({'est_price': nft_bank_est_value})