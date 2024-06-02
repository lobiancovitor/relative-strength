from datetime import date

import yfinance as yf

from load_data import get_securities

securities = get_securities()


def escape_ticker(ticker: str):  # Ex. -> POMO4.SA
    return ticker + ".SA" if ticker != "^BVSP" else ticker


def get_yf_data(ticker: str, start_date: date, end_date: date):
    escaped_ticker = escape_ticker(ticker)
    df = yf.download(
        escaped_ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
        repair=True,
    )

    candles = [
        {
            "open": row["Open"],
            "close": row["Close"],
            "low": row["Low"],
            "high": row["High"],
            "volume": row["Volume"],
            "datetime": int(idx.timestamp()),
        }
        for idx, row in df.iterrows()
    ]

    return {"data": candles}
