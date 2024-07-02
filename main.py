from golflive import processExcel, addRanking
from firestore import initializeDatabaseClient, writeToFirestore, generateCSV
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
                return 1
            case "Generate CSV":
                generateCSV(db)
            case "Exit":
                return
            case _:
                print("Invalid Input. Please try again")

if __name__ == "__main__":
    print(main())