import pandas as pd
import mappings

def processExcel(path):
    # Unnamed: 21 - Difference from PAR... This is the 20th column
    # GQSD 年中会员赛 - Names... This is also just the first column of the df (0)
    # First two rows are titles and there's an extra row at the bottom we don't care about
    df = pd.read_excel(path)
    df = df.iloc[2:-1, [0, 21]]
    df.columns = ['Names', 'Total Score']
    df['Total Score'] = df['Total Score'].astype(int)
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
        if df.loc[i, "Rank"] in mappings.rankToPointsMapping:
            df.loc[i, "FedEx Points"] = mappings.rankToPointsMapping[df.loc[i, "Rank"]]
    return df