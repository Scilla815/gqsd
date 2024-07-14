from golflive import processExcel, addRanking, updateMemberships
from firestore import initializeDatabaseClient, writeToFirestore, updateUserMembership, generateCSV, deleteUsers
import inquirer
import os

def main():
    db = initializeDatabaseClient()

    while True:
        questions = [
        inquirer.List('action',
                        message="What would you like to do?",
                        choices=["Process Scores", "Update Users", "Generate CSV", "Reset Database", "Exit"],
                    ),
        ]
        answers = inquirer.prompt(questions)
        userInput = answers["action"]
        match userInput:
            case "Process Scores":
                filename = input("Which match do you want to process? (Use 'All' to process all matches) ")
                if filename == "All":
                    df = processExcel("data/match_scores" + filename)
                    df = addRanking(df)
                    writeToFirestore(db, df)
                else:
                    folder_path = "data/match_scores"
                    for filename in os.listdir(folder_path):
                        df = processExcel(folder_path + filename)
                        df = addRanking(df)
                        writeToFirestore(db, df)
            case "Update Users":
                membershipDict = updateMemberships()
                updateUserMembership(db, membershipDict)
            case "Generate CSV":
                fileType = input("csv or xlsx? ")
                generateCSV(db, fileType)
            case "Reset Database":
                deleteUsers(db)
            case "Exit":
                return
            case _:
                print("Invalid Input. Please try again")

if __name__ == "__main__":
    main()