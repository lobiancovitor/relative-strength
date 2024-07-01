from datetime import datetime

import yfinance as yf


def get_yf_data(securities: list) -> dict:
    df = yf.download(securities, period="1y")

    candles = [
        {
            "open": round(float(row["Open"]), 3),
            "close": round(float(row["Close"]), 3),
            "low": round(float(row["Low"]), 3),
            "high": round(float(row["High"]), 3),
            "volume": round(float(row["Volume"]), 3),
            "datetime": datetime.fromtimestamp(
                int(idx.timestamp())).strftime(
                    "%Y-%m-%d"
                ),
        }
        for idx, row in df.iterrows()
    ]

    return {"data": candles}
