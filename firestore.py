import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import pandas as pd
import config

def initializeDatabaseClient():
    cred = credentials.Certificate(config.CRED_PATH)
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

def updateUserMembership(db, statusDict):
    for key in statusDict:
        user_ref = db.collection('users').document(key)
        if user_ref.get().exists:
            parsedDate = datetime.strptime(statusDict[key], '%b %Y')
            currentDate = datetime.now()
            activeSub = parsedDate + timedelta(days=365)
            data = {
                'last_paid': parsedDate,
                'isActive': currentDate < activeSub
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
    df = df.reindex(columns=["name", "runningYearlyTotal", "isActive", "last_paid"])
    csv_file_path = config.OUTPUT_PATH
    df.to_csv(csv_file_path, index=False)