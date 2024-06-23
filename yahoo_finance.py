from datetime import date

import yfinance as yf


def get_yf_data(securities: list, period="5y") -> dict:
    df = yf.download(
        securities,
    )

    candles = [
        {
            "open": row["Open"],
            "close": row["Adj Close"],
            "low": row["Low"],
            "high": row["High"],
            "volume": row["Volume"],
            "datetime": int(idx.timestamp()),
        }
        for idx, row in df.iterrows()
    ]

    return {"data": candles}
