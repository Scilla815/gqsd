import firebase_admin
from firebase_admin import credentials, firestore
import os
import pandas as pd

def initializeDatabaseClient():
    cred = credentials.Certificate("gqsd-91223-firebase-adminsdk-tqw24-12f3780010.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def writeToFirestore(db, df):
    for index, row in df.iterrows():
        user_ref = db.collection('users').document(row["Names"])
        data = {
            'name': row["Names"],
            'runningYearlyTotal': firestore.Increment(row["FedEx Points"])
        }
        user_ref.set(data, merge=True)

def generateCSV(db):
    collection_ref = db.collection("users")
    docs = collection_ref.stream()

    data = []
    for doc in docs:
        doc_dict = doc.to_dict()
        # doc_dict['id'] = doc.id
        data.append(doc_dict)

    df = pd.DataFrame(data)
    df = df.reindex(columns=["name", "runningYearlyTotal"])
    csv_file_path = "output/output.csv"
    df.to_csv(csv_file_path, index=False)