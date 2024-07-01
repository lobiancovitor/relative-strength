from fundamental.fundamental import get_fundamental_rating
from acc_dist.acc_dist import calculate_stock_ad
from strength.ranking import rankings
import pandas as pd
from .industry_group import get_industry_group

RS_COLUMNS          = ["Ticker", "RS Rating"]
FUNDAMENTAL_COLUMNS = ["Ticker","Fundamental Rating"]
AD_COLUMNS          = ["Ticker","A/D Rating"]
INDUSTRY_COLUMNS    = ["Ticker", "Industry Group"]

def create_dataframe(PRICE_DATA_FILE: str, REF_TICKER: dict):
    relative_strength =  rankings(PRICE_DATA_FILE, REF_TICKER)[RS_COLUMNS]
    fundamentals = get_fundamental_rating()[FUNDAMENTAL_COLUMNS]
    acc_dist = calculate_stock_ad(PRICE_DATA_FILE)[AD_COLUMNS]
    industry_group = get_industry_group()[INDUSTRY_COLUMNS]
    
    df = pd.merge(relative_strength, fundamentals, on='Ticker')
    df = pd.merge(df, acc_dist, on='Ticker')
    df = pd.merge(df, industry_group, on='Ticker')
    
    df['Master Score'] = df.apply(calculate_master_score, axis=1)
    
    df = df[["Ticker", "Master Score", "Fundamental Rating", "RS Rating", "A/D Rating", "Industry Group"]]
    
    df = df.sort_values(by='Master Score', ascending=False)
    
    df['Master Score'] = df['Master Score'].apply(map_master_score_to_grade)
    
    df['Ticker'] = df['Ticker'].str.replace(r'\.SA$', '')
    
    return df

def calculate_master_score(row):
    fundamental_score_map = {
        'A+': 4, 'A': 3, 'B+': 2.5, 'B': 2, 'C+': 1.5, 'C': 1, 'D+': 0.5, 'D': 0, 'E': 0
    }
    
    ad_score_map = {
        'A+': 4, 'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0
    }
    
    fundamental_score = fundamental_score_map.get(row['Fundamental Rating'], 0)
    ad_score = ad_score_map.get(row['A/D Rating'], 0)

    rs_rating = row['RS Rating']
    if rs_rating > 80:
        rs_score = 4
    elif rs_rating > 70:
        rs_score = 3
    elif rs_rating > 50:
        rs_score = 2
    else:
        rs_score = 1
    
    master_score = (fundamental_score * 2) + (rs_score * 1.5) + ad_score
    
    return master_score

def map_master_score_to_grade(score):
    if score >= 14:
        return 'A+'
    elif score >= 12:
        return 'A'
    elif score >= 9:
        return 'B'
    elif score >= 6:
        return 'C'
    elif score >= 3:
        return 'D'
    else:
        return 'E'