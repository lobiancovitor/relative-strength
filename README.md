# RS Rating
IBD Style Relative Strength Percentile Ranking of Stocks for Brazilian Markets (i.e. 0-99 Score)  

[Relative Strength Rating Pinpoints A Stock's Power](https://finance.yahoo.com/news/relative-strength-rating-pinpoints-stocks-214500318.html)

## Daily Generated Outputs
https://github.com/lobiancovitor/relative-strength/blob/main/output/rs_stocks.csv  

## [Market Breadth](https://github.com/lobiancovitor/relative-strength/blob/main/breadth/README.md)
Market breadth attempts to find how much underlying strength or weakness there is in a given stock index. Decades of market history show three out of four stocks will follow the underlying trend, either up or down.

## Calculation
Yearly performance of stock divided by IBOV performance during the same period.  
Based on Fred6725 work.  

RS Score = 40% * P3 + 20% * P6 + 20% * P9 + 20% * P12

With P3 the performance of the 3 last month. (P3 = Close/Close[63], for 63 days back)

Formula: RS Score = (1 + RS Score for Stocks) / (1 + RS Score for IBOV)

Then all stocks are ranked from largest to smallest and a percentile is assigned from 99 to 0.


# Fundamental Rating
Single assessment of a company's earnings and key fundamentals.  
This rating measures quarterly earnings growth, gross margins and gross profitability.  

[An explanation on earnings growth](https://finance.yahoo.com/news/eps-rating-fast-tracks-basic-221200776.html)  

[The other side of value: The gross profitability premium, Robert Novy-Marx](https://www.sciencedirect.com/science/article/abs/pii/S0304405X13000044)
  

## Considered Stocks
Tickers from https://www.dadosdemercado.com.br/bolsa/acoes


### Run Python Script

1. Install requirements: `python -m pip install -r requirements.txt`
2. Run `main.py`


### \*\*\* Output \*\*\*

- in the `output` folder you will find the list of ranked stocks: `rs_stocks.csv`
