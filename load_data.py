import pandas as pd

DATA_URL = "https://www.dadosdemercado.com.br/bolsa/acoes"
FPATH = "data/fundamentals.csv"


def escape_ticker(ticker: str):  # Ex. -> POMO4.SA
    return ticker + ".SA" if ticker != "^BVSP" else ticker


def get_securities(data_url: str = DATA_URL) -> list:
    collection = pd.read_html(data_url)

    if not collection:
        raise Exception("Could not find a table...")

    # You can also save this locally
    # for index, table in enumerate(collection):
    #     table.to_csv(f"collection_{index}.csv")

    securities = list(collection[0]["Ticker"].values)
    # securities = collection[0]["Ticker"][:20].values  # Usar em testes

    return list(map(escape_ticker, securities))


def get_fundamentals(path: str = FPATH):
    return pd.read_csv(path)
