import pandas as pd

DATA_URL = "https://www.dadosdemercado.com.br/bolsa/acoes"


def get_securities(data_url: str = DATA_URL) -> list:
    collection = pd.read_html(data_url)

    if not collection:
        raise Exception("Could not find a table...")

    # You can also save this locally
    # for index, table in enumerate(collection):
    #     table.to_csv(f"collection_{index}.csv")

    # securities = collection[0]["Ticker"].values
    securities = collection[0]["Ticker"][:20].values  # Usar em testes

    return list(securities)
