import json
from gql.transport import requests
import requests

from my_package.polling_bot import start_telegram_poll
from my_package.global_var import db, total_gov_token

# nft_bank api setup
nft_bank_api = 'b8bb9504e550e732265f08434414b8dd'
headers = {'x-api-key': nft_bank_api}


# update nft_holdings' estimates periodically
def update_est_prices(updater, dispatcher):
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

            if nft_bank_est_value > float(nft["est_price"]):
                db.collection('nft_holdings').document(key).update({'price_high': nft_bank_est_value})
            elif (nft['price_high'] - nft_bank_est_value) / nft['price_high'] > 0.3:
                print("당장 팔아요!")

                data = {'project': nft['project'],
                        'project_address': nft['project_address'],
                        'chain': nft['chain'],
                        'token_id': nft['token_id'],
                        'category': nft['category'],
                        'price_buy': nft['price_buy'],
                        'price_est': nft_bank_est_value,
                        'is_buy_poll': False,
                        'consent_token_amount': 0,
                        'quorum': total_gov_token * (1 / 2),
                        'consent_list': [],
                        'reject_list': [],
                        'price_high': nft['price_high']
                        }

                poll_id = start_telegram_poll(updater, dispatcher, data)

                del data['price_high']
                data['poll_id'] = poll_id
                db.collection('nft_pendings').add(data)
