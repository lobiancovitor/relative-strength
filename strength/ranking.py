import pandas as pd

from utils import read_json

MIN_PERCENTILE = 0

TITLE_RANK = "Rank"
TITLE_TICKER = "Ticker"
TITLE_PERCENTILE = "RS Rating"
TITLE_1M = "1 Month Ago"
TITLE_3M = "3 Months Ago"
TITLE_6M = "6 Months Ago"
TITLE_RS = "Relative Strength"


def relative_strength(closes: pd.Series, closes_ref: pd.Series):
    rs_stock = strength(closes)
    rs_ref = strength(closes_ref)
    rs = (1 + rs_stock) / (1 + rs_ref) * 100
    rs = int(rs * 100) / 100  # round to 2 decimals
    return rs


def strength(closes: pd.Series):
    """Calculates the performance of the last year (most recent quarter is weighted double)"""
    try:
        quarters1 = quarters_perf(closes, 1)
        quarters2 = quarters_perf(closes, 2)
        quarters3 = quarters_perf(closes, 3)
        quarters4 = quarters_perf(closes, 4)
        return 0.4 * quarters1 + 0.2 * quarters2 + 0.2 * quarters3 + 0.2 * quarters4
    except Exception:
        return 0


def quarters_perf(closes: pd.Series, n):
    length = min(len(closes), n * int(252 / 4))
    prices = closes.tail(length)
    pct_chg = prices.pct_change().dropna()
    perf_cum = (pct_chg + 1).cumprod() - 1
    return perf_cum.tail(1).item()


def rankings(price_data_file: str, reference_ticker: dict):
    """Returns a dataframe with percentile rankings for relative strength"""
    json = read_json(price_data_file)
    relative_strengths = []
    ranks = []
    stock_rs = {}

    for ticker in json:
        try:
            closes = list(map(lambda data: data["close"], json[ticker]["data"]))
            closes_ref = list(
                map(lambda data: data["close"], reference_ticker["ticker"]["data"])
            )

            if len(closes) >= 6 * 20:
                closes_series = pd.Series(closes)
                closes_ref_series = pd.Series(closes_ref)
                rs = relative_strength(closes_series, closes_ref_series)
                month = 20
                tmp_percentile = 100
                rs1m = relative_strength(
                    closes_series.head(-1 * month), closes_ref_series.head(-1 * month)
                )
                rs3m = relative_strength(
                    closes_series.head(-3 * month), closes_ref_series.head(-3 * month)
                )
                rs6m = relative_strength(
                    closes_series.head(-6 * month), closes_ref_series.head(-6 * month)
                )

                if rs < 600:
                    # stocks output
                    ranks.append(len(ranks) + 1)
                    relative_strengths.append(
                        (0, ticker, rs, tmp_percentile, rs1m, rs3m, rs6m)
                    )
                    stock_rs[ticker] = rs

        except KeyError:
            print(f"Ticker {ticker} has corrupted data.")

    # stocks
    df = pd.DataFrame(
        relative_strengths,
        columns=[
            TITLE_RANK,
            TITLE_TICKER,
            TITLE_RS,
            TITLE_PERCENTILE,
            TITLE_1M,
            TITLE_3M,
            TITLE_6M,
        ],
    )
    df[TITLE_PERCENTILE] = pd.qcut(df[TITLE_RS], 100, labels=False, duplicates="drop")
    df[TITLE_1M] = pd.qcut(df[TITLE_1M], 100, labels=False, duplicates="drop")
    df[TITLE_3M] = pd.qcut(df[TITLE_3M], 100, labels=False, duplicates="drop")
    df[TITLE_6M] = pd.qcut(df[TITLE_6M], 100, labels=False, duplicates="drop")
    df = df.sort_values(([TITLE_RS]), ascending=False)
    df[TITLE_RANK] = ranks
    out_tickers_count = 0
    for index, row in df.iterrows():
        if row[TITLE_PERCENTILE] >= MIN_PERCENTILE:
            out_tickers_count = out_tickers_count + 1
    df = df.head(out_tickers_count)

    return df
