import pandas as pd

FPATH = "data/fundamentals.csv"


def get_fundamental_rating(path: str = FPATH):
    df = pd.read_csv(path)
    
    df["Ticker"] = df["Ticker"].apply(lambda x: x + ".SA")
    
    return df
