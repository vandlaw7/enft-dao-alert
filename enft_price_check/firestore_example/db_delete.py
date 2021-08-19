import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Setup
cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Delete data - known id
# db.collection('persons').document('p1').delete()

# Delete data - known id - field
# db.collection('persons').document('p2').update({"socials": firestore.DELETE_FIELD})

# Delete docs -unknown ID : first way
docs = db.collection('persons').get()
for doc in docs:
    key = doc.id
    db.collection('persons').document(key).delete()

# docs = db.collection('persons').where("age", ">=", 40).get()
# for doc in docs:
#     key = doc.id
#     db.collection('persons').document(key).update({'age': firestore.DELETE_FIELD})
