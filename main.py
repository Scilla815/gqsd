import firebase_admin
from firebase_admin import credentials, firestore
from golflive import processExcel, addRanking

cred = credentials.Certificate("gqsd-91223-firebase-adminsdk-tqw24-12f3780010.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

df = processExcel('data/match_score_2.xlsx')
df = addRanking(df)

print(df)