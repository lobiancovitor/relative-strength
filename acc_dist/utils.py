def up_down_ratio(data, ticker):
    volume_data = list(map(lambda data: data["volume"], data))[
        -50:
    ]
    price_data = list(map(lambda data: data["close"], data))[
        -50:
    ]

    up_volume = 0
    down_volume = 0

    for i in range(1, len(price_data)):
        if price_data[i] > price_data[i - 1]:
            up_volume += volume_data[i]
        else:
            down_volume += volume_data[i]

    ratio = up_volume / down_volume if down_volume != 0 else 0

    if ratio is not None:
        ratio = round(ratio, 1)

    return ratio


def calculate_cr(data):
    try:
        return round(
            (data["close"] - data["low"]) / (data["high"] - data["low"]) * 100, 2
        )
    except Exception:
        return 0


def classify_score(score):
    if score >= 30:
        return "A+"
    elif score >= 15:
        return "A"
    elif score >= 0:
        return "B"
    elif score >= -15:
        return "C"
    elif score >= -30:
        return "D"
    else:
        return "E"


def weight_score(total_score, ud_ratio):
    if ud_ratio >= 2:
        total_score *= 1.35
    elif ud_ratio > 1.5:
        total_score *= 1.3
    elif ud_ratio >= 1.2:
        total_score *= 1.2
    elif ud_ratio < 0.5:
        total_score *= 0.8
    elif ud_ratio < 0.8:
        total_score *= 0.85

    return total_score
