import pandas as pd

mapping = {
    1: 500,
    2: 300,
    3: 190,
    4: 135,
    5: 110,
    6: 100,
    7: 90,
    8: 85,
    9: 80,
    10: 75,
    11: 70,
    12: 65,
    13: 60,
    14: 57,
    15: 55,
    16: 53,
    17: 51,
    18: 49,
    19: 47,
    20: 45,
    21: 43,
    22: 41,
    23: 39,
    24: 37,
    25: 35.5,
    26: 34,
    27: 32.5,
    28: 31,
    29: 29.5,
    30: 28,
    31: 26.5,
    32: 25,
    33: 23.5,
    34: 22,
    35: 21,
    36: 20,
    37: 19,
    38: 18,
    39: 17,
    40: 16,
    41: 15,
    42: 14,
    43: 13,
    44: 12,
    45: 11,
    46: 10.5,
    47: 10,
    48: 9.5,
    49: 9,
    50: 8.5
}

def processExcel(path):
    # Unnamed: 21 - Difference from PAR... This is the 20th column
    # GQSD 年中会员赛 - Names... This is also just the first column of the df (0)
    # First two rows are titles and there's an extra row at the bottom we don't care about
    df = pd.read_excel(path)
    df = df.iloc[2:-1, [0, 21]]
    df.rename(columns={'Unnamed: 21': 'Total Score'}, inplace=True)
    df['Total Score'] = df['Total Score'].astype(int)
    return df

def addRanking(df):
    df.sort_values(by='Total Score', inplace=True)
    df = df.reset_index()
    df["Rank"] = df.index + 1 
    for i in range(1, len(df)):
        if df.loc[i, "Total Score"] == df.loc[i-1, "Total Score"]:
            df.loc[i, "Rank"] = df.loc[i-1, "Rank"]
    return df