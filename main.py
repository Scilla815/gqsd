from golflive import processExcel, addRanking
from firestore import initializeDatabaseClient, writeToFirestore, generateCSV

db = initializeDatabaseClient()

df = processExcel('data/match_score_3.xlsx')
df = addRanking(df)

print(df)
    
# writeToFirestore(db, df)

print(generateCSV(db))

# print(db)