import os
from datetime import date, timedelta

from load_data import get_securities
from utils import write_to_file
from yahoo_finance import get_yf_data

from breadth.load_data import get_data
from breadth.breadth import breadth

from composite import composite as c

today = date.today()
start_date = today - timedelta(days=1 * 365 + 183)

DIR = os.getcwd()
DATA_DIR = os.path.join(DIR, "data")
OUTPUT_DIR = os.path.join(DIR, "output")
PRICE_DATA_FILE = os.path.join(OUTPUT_DIR, "price_history.json")
REFERENCE_TICKER = get_yf_data("^BVSP")
REF_TICKER = {"ticker": REFERENCE_TICKER}

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_data(securities: list):
    tickers_data = {
        ticker: get_yf_data(ticker) for ticker in securities
    }
    write_to_file(tickers_data, PRICE_DATA_FILE)


def main():
    securities = get_securities()
    save_data(securities)
    df = c.create_dataframe(PRICE_DATA_FILE, REF_TICKER)
    df.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "ratings.csv",
        ),
        index=False,
    )
    data = get_data(securities)
    breadth(data, len(securities))
    print("***\nYour 'ratings.csv' is in the output folder.\n***")


if __name__ == "__main__":
    main()
