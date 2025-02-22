import pandas as pd
import mappings
import config

def processExcel(path):
    # Unnamed: 21 - Difference from PAR... This is the 20th column
    # GQSD 年中会员赛 - Names... This is also just the first column of the df (0)
    # First two rows are titles and there's an extra row at the bottom we don't care about
    df = pd.read_excel(path)
    df = df.iloc[2:-1, [0, 21]]
    df.columns = ['Names', 'Total Score']
    df['Total Score'] = df['Total Score'].astype(int)
    df = df.reset_index(drop=True)
    nicknameMapping = createNicknameMapping()
    for index, row in df.iterrows():
        if row["Names"] in nicknameMapping:
            df.iloc[index, df.columns.get_loc('Names')] = nicknameMapping[row["Names"]]
    return df

def addRanking(df):
    df.sort_values(by='Total Score', inplace=True)
    df = df.reset_index()
    df["Rank"] = df.index + 1
    df["FedEx Points"] = 0
    df.loc[0, "FedEx Points"] = 500
    for i in range(1, len(df)):
        if df.loc[i, "Total Score"] == df.loc[i-1, "Total Score"]:
            df.loc[i, "Rank"] = df.loc[i-1, "Rank"]
        if df.loc[i, "Rank"] in mappings.FedExMapping:
            df.loc[i, "FedEx Points"] = mappings.FedExMapping[df.loc[i, "Rank"]]
    return df

def updateMemberships():
    filePath = config.MEMBERS_PATH
    df = pd.read_excel(filePath, sheet_name=None)
    nicknameMapping = createNicknameMapping()
    membershipStatusDict = {}
    for sheet in df.keys():
        if sheet != "Mappings":
            for index, row in df[sheet].iterrows():
                if row["Member Fee"] and not pd.isna(row["Member Fee"]):
                    if row["Name"] in nicknameMapping:
                        membershipStatusDict[nicknameMapping[row["Name"]]] = sheet
                    else:
                        membershipStatusDict[row["Name"]] = sheet
    return membershipStatusDict

def createNicknameMapping():
    filePath = config.MEMBERS_PATH
    mapping_dict = {}
    df = pd.read_excel(filePath, sheet_name="Mappings")

    for index, row in df.iterrows():
        # The first element in the row is the key
        name = row[0]
        # The rest of the row (excluding NaN values) is the value
        nicknames = row[1:].dropna().tolist()
        # Add the key-value pair to the dictionary
        for nickname in nicknames:
            mapping_dict[nickname] = name

    return mapping_dict