import json

import requests
from firebase_admin import firestore
from gql.transport import requests

from my_package.global_var import db, total_gov_token
from my_package.polling_bot import start_telegram_poll

# nft_bank api setup
nft_bank_api = 'b8bb9504e550e732265f08434414b8dd'
headers = {'x-api-key': nft_bank_api}


# update nft_holdings' estimates periodically
def update_price_estimations(updater, dispatcher):
    chat_ids = db.collection('global').document('global').get().to_dict()["chat_list"]
    for chat_id in chat_ids:
        docs = db.collection('dao').document(chat_id).collection('nft_holdings').get()
        for doc in docs:
            nft = doc.to_dict()
            price_check_url = f'https://api.nftbank.ai/estimates-v2/estimates/' \
                              f'{nft["project_address"]}/{nft["token_id"]}?chain_id={nft["chain"].upper()}'
            r = requests.get(price_check_url, headers=headers)
            estimated_result = json.loads(r.text)
            # 이미 NFTbank estimation을 바탕으로 구매했던 NFT이기 때문에 NFTbank에서 계속 estimation 을 해준다고 가정함.
            nft_bank_est_value = float(estimated_result['data'][0]['estimate'][0]['estimate_price'])
            print(nft['price_high'], nft_bank_est_value)
            print((nft['price_high'] - nft_bank_est_value) / nft['price_high'])
            print((nft['price_high'] - nft_bank_est_value) / nft['price_high'] > 0.3)
            if nft_bank_est_value != float(nft["price_est"]):
                key = doc.id
                db.collection('dao').document(chat_id).collection('nft_holdings').document(key).update(
                    {'price_est': nft_bank_est_value})
                # array 없으면 자동으로 array 만들어줌.
                db.collection('dao').document(chat_id).collection('nft_holdings').document(key).update(
                    {'est_history': firestore.ArrayUnion([nft_bank_est_value])})
                if nft_bank_est_value > float(nft["price_high"]):
                    db.collection('dao').document(chat_id).collection('nft_holdings').document(key).update(
                        {'price_high': nft_bank_est_value})
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

                    poll_id = start_telegram_poll(updater, dispatcher, data, chat_id)

                    del data['price_high']
                    data['poll_id'] = poll_id
                    db.collection('dao').document(chat_id).collection('nft_pendings').add(data)
                    db.collection('global').document('global').update(
                        {'poll_list': firestore.ArrayUnion([poll_id])})
                    db.collection('global').document('poll_index').update({str(poll_id): chat_id})
