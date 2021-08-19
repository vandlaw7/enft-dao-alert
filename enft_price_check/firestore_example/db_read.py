import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Setup
cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# getting a document with a known ID
result = db.collection('global').document('global').get()
if result.exists:
    print(result.to_dict())

# Get all documents in a collection
'''docs = db.collection('persons').get()
for doc in docs:
    print(doc.to_dict())'''

# Querying
# docs = db.collection('persons').where("age", ">=", 40).get()
'''docs = db.collection('persons').where("socials", "array_contains", "linkedin").get()
for doc in docs:
    print(doc.to_dict())'''
# == != > < >= <= all possible.

docs = db.collection('persons').where('address', 'in', ["London", "Milan"]).get()
for doc in docs:
    print(doc.to_dict())
