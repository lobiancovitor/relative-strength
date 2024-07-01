import pandas as pd
from .utils import classify_score, calculate_cr, up_down_ratio, weight_score
from utils import read_json

def calculate_stock_ad(price_data_file: str):
    tickers_data = read_json(price_data_file)
    scores = {}
    ratings = []
    for ticker in tickers_data:
        daily_scores = []
        volume_data = list(
            map(lambda data: data["volume"], tickers_data[ticker]["data"])
        )
        volume_series = pd.Series(volume_data)
        ma_vol = volume_series.rolling(window=50).mean()
        data = tickers_data[ticker]["data"]

        for i in range(1, len(data)):
            stock_score = 0
            volume_score = 0
            volume = list(map(lambda data: data["volume"], data))[i]
            close = list(map(lambda data: data["close"], data))[i]
            previous_close = list(map(lambda data: data["close"], data))[i - 1]
            closing_range = calculate_cr(data[i])
            volume_change = volume / ma_vol.iloc[i]

            if close >= previous_close:
                if volume > ma_vol.iloc[i]:
                    volume_score += 2
                elif volume < ma_vol.iloc[i] * 0.7:
                    volume_score += 1
                else:
                    volume_score += 1.5

                if close >= previous_close * 1.03:
                    stock_score += 1
                if closing_range >= 60:
                    stock_score += 1

            if close < previous_close:
                if volume > ma_vol.iloc[i]:
                    volume_score -= 2
                elif volume < ma_vol.iloc[i] * 0.7:
                    volume_score -= 1
                else:
                    volume_score -= 1.5

                if close <= previous_close * 0.97:
                    stock_score -= 1
                if closing_range <= 45:
                    stock_score -= 1

            if volume_change > 3:
                volume_score = 3.5 if close > previous_close else -3.5
            elif volume_change > 2:
                volume_score = 3 if close > previous_close else -3
            elif volume_change > 1.5:
                volume_score = 2.5 if close > previous_close else -2.5

            daily_score = stock_score + volume_score
            daily_scores.append(daily_score)
        total_score = sum(daily_scores[-126:])
        ud_ratio = up_down_ratio(data, ticker)

        total_score = weight_score(total_score, ud_ratio)

        scores[ticker] = classify_score(total_score)
        ratings.append((ticker, classify_score(total_score)))

    df = pd.DataFrame(
        ratings,
        columns=["Ticker", "A/D Rating"],
    )

    #df["Ticker"] = df["Ticker"].str.replace(".SA", "")

    return df
