import yfinance as finance
import pandas as pd
import os

def generate_dataset():
    os.makedirs("storage", exist_ok=True)
    crypto_data = finance.Ticker("BTC-USD").history(period="max")

    crypto_data.index = pd.to_datetime(crypto_data.index).date
    crypto_data.index = pd.to_datetime(crypto_data.index)

    del crypto_data["Dividends"]
    del crypto_data["Stock Splits"]

    crypto_data.columns = [col.lower() for col in crypto_data.columns]
    crypto_data['next_day'] = crypto_data['close'].shift(-1)
    crypto_data['movement'] = crypto_data['next_day'].pct_change() * 100
    crypto_data.drop(['next_day'], axis=1, inplace=True)

    extra_assets = "^GSPC ^DJI ^N225 ^N100 000001.SS CL=F GC=F HG=F NVDA AAPL"
    extra_data = finance.download(extra_assets, start="2014-09-17").Close

    extra_data.fillna(method='ffill', inplace=True)
    merged_data = crypto_data.merge(extra_data, left_index=True, right_index=True, how='left')
    merged_data.fillna(method='ffill', inplace=True)
    merged_data.dropna(inplace=True)

    merged_data.to_csv("storage/dataset.csv")
    return merged_data

if __name__ == '__main__':
    generate_dataset()
