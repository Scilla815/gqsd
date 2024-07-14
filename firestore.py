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

def generateCSV(db, fileType):
    collection_ref = db.collection("users")
    docs = collection_ref.stream()

    data = []
    for doc in docs:
        doc_dict = doc.to_dict()
        # doc_dict['id'] = doc.id
        data.append(doc_dict)

    df = pd.DataFrame(data)
    df = df.reindex(columns=["name", "runningYearlyTotal", "isActive", "last_paid"])
    match fileType:
        case "csv":
            csv_file_path = config.OUTPUT_PATH + ".csv"
            df.to_csv(csv_file_path, index=False)
        case "xlsx":
            df["last_paid"] = df["last_paid"].dt.tz_convert(None)
            xlsx_file_path = config.OUTPUT_PATH + ".xlsx"
            df.to_excel(xlsx_file_path, index=False)
        case _:
            return "Invalid file type"

def deleteUsers(db, collection_name):
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()

    confirmation = input(f"Are you sure you want to delete {collection_name} collection? (Yes/No) ")

    if confirmation == "Yes":
        for doc in docs:
            doc.reference.delete()

        print(f"{collection_name} Deleted")

    print("Deletion Cancelled")