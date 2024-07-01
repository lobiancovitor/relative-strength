import pandas as pd

FPATH = "data/industry_group.csv"


def get_industry_group(path: str = FPATH):
    df = pd.read_csv(path, encoding="latin1")

    df = df.iloc[:, -2:]
    df.columns = ["Ticker", "Industry Group"]

    df["Ticker"] = df["Ticker"].apply(lambda x: x + ".SA")

    return df
