import yfinance as yf
import pandas as pd
from datetime import timedelta
from datetime import datetime
from datetime import date
import os

tickers = pd.read_csv('C:\\Users\\chlsp\\Desktop\\Stocks\\StockList.csv')
extension = 'NS'
symbols = tickers.Symbol + '.' + extension


def calculate_PL_percentage(data):
    percentages = pd.DataFrame({'date': [], 'percentage': []})
    for i in data.index:
        if i == 0:
            percentages = percentages.append(
                {'date': data['Date'][i], 'percentage': 0}, ignore_index=True)
        else:
            percentages = percentages.append({'date': data['Date'][i], 'percentage': round(
                ((data['Adj Close'][i] - data['Adj Close'][i-1])/data['Adj Close'][i-1])*100, 2)}, ignore_index=True)
    return percentages


def strptime_with_offset(date, format='%d-%m-%Y'):
    base_dt = datetime.strftime(date, format)
    return base_dt


all_stock_data = pd.DataFrame()

for i in symbols.index:
    try:
        data = yf.download(
            symbols[i], start="2016-01-01", end="2021-02-23")
        data.dropna(how='all', inplace=True)
        print("%d out of %d completed" % (i+1, len(symbols)))
        data.reset_index(drop=False, inplace=True)
        all_stock_data[symbols[i]] = data['Adj Close']
    except:
        print("error extracting symbol %s" % (symbols[i]))

today = date.today()
try:
    os.mkdir('D:\\Stocks\\{}'.format(today))
except OSError as error:
    print(error)
path = "D:\\Stocks\\" + str(today) + "\\stocks_{0}.xlsx".format(today)
all_stock_data.to_excel(path, index=False)
