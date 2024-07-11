from golflive import processExcel, addRanking, updateMemberships
from firestore import initializeDatabaseClient, writeToFirestore, updateUserMembership, generateCSV
import inquirer

def main():
    db = initializeDatabaseClient()

    while True:
        questions = [
        inquirer.List('action',
                        message="What would you like to do?",
                        choices=["Process Scores", "Update Users", "Generate CSV", "Exit"],
                    ),
        ]
        answers = inquirer.prompt(questions)
        userInput = answers["action"]
        match userInput:
            case "Process Scores":
                filename = input("Which match do you want to process? ")
                df = processExcel("data/" + filename)
                df = addRanking(df)
                writeToFirestore(db, df)
            case "Update Users":
                membershipDict = updateMemberships()
                updateUserMembership(db, membershipDict)
            case "Generate CSV":
                fileType = input("csv or xlsx? ")
                generateCSV(db, fileType)
            case "Exit":
                return
            case _:
                print("Invalid Input. Please try again")

if __name__ == "__main__":
    main()