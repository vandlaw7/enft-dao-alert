import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# db.collection('persons').add({'name': 'John', 'age': 40})

# Add document with auto IDs
data = {'name': 'John Smith', 'age': 40, 'employed': True}
data2 = {'name': 'Jane Doe', 'age': 34, 'employed': False}
# If you write code like below, same data with different id will be generated in DB again ang again
# when you run the code again.
# db.collection('people').add(data2)

# Set documents with Known IDs
data3 = {'name': 'Jane Doe', 'age': 34, 'employed': False}
# with document reference like below, you can have unique data with unique id.
# although you run the below code again, there is only one document named 'janedoe'
# db.collection('persons').document('janedoe').set(data3)  # document reference

# Set documents with auto IDs
# db.collection('persons').document().set(data3)


# Merging
# db.collection('persons').document('janedoe').set({'address': 'London'}, merge=True)

# creating sub-collection
# db.collection('persons').document('janedoe').collection('movies').add({'name': 'Avengers'})
# db.collection('persons').document('janedoe').collection('movies').document('HP').set({'name': 'Harry Porter'})

# practice for making same db with video #3's start
# db.collection('persons').add({'address': 'Milan', 'age': 40, 'name': 'Ron'})
# db.collection('persons').add({'address': 'Paris', 'age': 42, 'name': 'Jang'})
# db.collection('persons').add({'address': 'Berlin', 'age': 38, 'name': 'Hans'})
# db.collection('persons').add({'address': 'Madrid', 'age': 36, 'name': 'Gabriel'})
# db.collection('persons').document('p1').set({'age': 21, 'name': 'sam',
#                                              'socials': ['youtube', 'linkedin', 'github']})
# db.collection('persons').document('p2').set({'age': 25, 'name': 'megan',
#                                              'socials': ['youtube', 'instagram', 'twitter']})
# db.collection('persons').add({'address': 'London', 'age': 34, 'name': 'Jane'})


