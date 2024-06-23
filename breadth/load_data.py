import pandas as pd
import yfinance as yf

DATA_URL = "https://www.dadosdemercado.com.br/bolsa/acoes"


def get_data(securities: list):
    return yf.download(securities, period="5y")["Adj Close"]
