# GQSD Data Project

## Description

This project serves to act as a backend for the GQSD golf group. The purpose of this project is to programatically take in golf tournament scores (via golflive) and process these scores for each user to keep a running total for the year. This also tracks the membership status of each golfer, listing when they last paid their membership fees and whether their membership is active.

## Requirements

- Python 3.x

## Setup

Follow these steps to set up and run your app:

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/gqsd.git
   cd gqsd
   ```
2. **Setup Environment (optional but recommended)**
    ```sh
    python3 -m venv env
    source env/bin/activate
    ```
3. **Installing Dependencies**
    ```sh
    pip install -r requirements.txt
    ```
4. **Running the App**
    ```sh
    python main.py
    ```
    This will open up a menu which gives you options to choose from
    1. *Process Scores* - Takes in an input for tournament file name to be processed and adds the scores to each players running yearly total
    2. *Update Users* - Reads information from the membership data and updates the status of golfers memberships
    3. *Generate CSV* - Takes the information from the database and extracts a CSV for ease of access via Google Sheets or Excel. Writes to output folder and overwrites existing output file
    4. *Exit* - Exits the app
5. Future Goals
    1. *Integrate with Front End* - Integrate this backend with the current GoDaddy front end.
    2. *Create Forms for Data Input* - Right now, the current method of obtaining data is very inconsistent in formatting and quality. If we create a form for golfers to submit information, it will ease development time.
    3. *More Granular Data for Tournaments* - Currently only tracking running yearly total. It would be beneficial to keep individual tournament results for players as well. Beneficial for both future development as well as ease of access for tournament data.
    4. *Adding Users who Paid Fee but no Tournaments* - Currently I'm not including people who have paid the membership fee but haven't played in a tournament. The correct behavior would be to initialize scores at 0, but because the name to nickname list has not been finalized, I have not implemented this yet.