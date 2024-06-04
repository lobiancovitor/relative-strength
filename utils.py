import json
import pandas as pd


def read_json(json_file):
    with open(json_file, "r", encoding="utf-8") as fp:
        return json.load(fp)


def write_to_file(data: dict, file_path: str):
    with open(file_path, "w", encoding="utf8") as fp:
        json.dump(data, fp, ensure_ascii=False)


def merge_dataframes(df1, df2):
    df = pd.merge(
        df1,
        df2,
        left_on="Ticker",
        right_on="ticker",
        how="left",
    ).drop(
        "ticker",
        axis=1,
    )

    df["Fundamental Rating"].fillna("N/A", inplace=True)

    return df
