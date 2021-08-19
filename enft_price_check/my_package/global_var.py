import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

nft_bank_api_key = 'b8bb9504e550e732265f08434414b8dd'
headers_for_nft_bank = {'x-api-key': nft_bank_api_key}

total_gov_token = 10000
