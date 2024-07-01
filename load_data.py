import pandas as pd

DATA_URL = "https://www.dadosdemercado.com.br/bolsa/acoes"


def enrich_ticker(ticker: str):
    return ticker + ".SA" if ticker != "^BVSP" else ticker


def get_securities(data_url: str = DATA_URL) -> list:
    collection = pd.read_html(data_url)

    if not collection:
        raise Exception("Could not find a table...")

    securities = list(collection[0]["Ticker"].values)
    # securities = collection[0]["Ticker"][:50].values  # Usar em testes

    return list(map(enrich_ticker, securities))
