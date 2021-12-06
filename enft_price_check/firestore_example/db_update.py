import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Setup
cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Update data - known key
# db.collection('persons').document('p1').update({'age': 50})
# adding new field is possible by update method
# db.collection('persons').document('p1').update({'address': 'London'})
# db.collection('persons').document('p1').update({'age': firestore.Increment(10)})
# db.collection('persons').document('p2').update({'address': 'London'})
# db.collection('persons').document('p2').update({'socials': firestore.ArrayRemove(["twitter"])})
db.collection('persons').document('p2').update(
    {'socials': firestore.ArrayUnion(["twitter"])})

# Update data - Unknown key
# First way
docs = db.collection('persons').g1et()
'''for doc in docs:
    if doc.to_dict()['age'] >= 36:
        key = doc.id
        # if key contains '-' or ' ' ', you will get some errors.
        db.collection('persons').document(key).update({"age_group": "middle_age"})'''

# Second way - effective
docs = db.collection('persons').where("age", ">=", 40).get()
for doc in docs:
    key = doc.id
    db.collection('persons').document(key).update(
        {"age_group": "older than 50 "})
