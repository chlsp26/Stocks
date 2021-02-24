import yfinance as yf
import pandas as pd
from datetime import timedelta
from datetime import datetime
from datetime import date
import data as d
import os

tickers = pd.read_csv('C:\\Users\\chlsp\\Desktop\\Python\\EQUITY_L.csv')
extension = 'NS'
symbols = tickers.SYMBOL + '.' + 'NS'

today = date.today()

def calculate_PL_percentage(data):
    percentages = pd.DataFrame({'dateTime':[], 'percentage': []})
    for i in data.index:
        if i == 0:
            percentages = percentages.append({'dateTime': data['Datetime'][i], 'percentage': round(((data['Close'][i] - data['Open'][i])/data['Open'][i])*100,2)}, ignore_index=True)
        else:
            percentages = percentages.append({'dateTime': data['Datetime'][i], 'percentage': round(((data['Close'][i] - data['Close'][i-1])/data['Close'][i-1])*100,2)}, ignore_index=True)
    return percentages

def strptime_with_offset(date, format='%H:%M:%S'):
    base_dt = datetime.strftime(date, format)
    return base_dt

all_stock_data = pd.DataFrame()
LTP = pd.Series([])
Open = pd.Series([])
Total = pd.Series([])
Change = pd.Series([])
for i in symbols.index:
    try:
        stock = yf.Ticker(symbols[i])
        data = stock.history(period="1d", interval=d.interval)
        previousDayData = yf.download(symbols[i], start=d.previousDayDate, end=d.todaysDate)
        data.dropna(how='all',inplace=True)
        previousDayData.dropna(how='all',inplace=True)
        print("%d out of %d completed" % (i+1, len(symbols)))
        data.reset_index(drop=False, inplace=True)
        previousDayData.reset_index(drop=False, inplace=True)
        if len(all_stock_data) == 0:
            all_stock_data = calculate_PL_percentage(data)
            all_stock_data.rename(columns = {'percentage':symbols[i]}, inplace=True)
        else:
            all_stock_data = pd.merge(all_stock_data, calculate_PL_percentage(data), how='left', on='dateTime')
            all_stock_data.rename(columns = {'percentage':symbols[i]}, inplace=True)
        Total[symbols[i]] = all_stock_data[symbols[i]].sum()
        Open[symbols[i]] = round(data['Open'][0],2)
        LTP[symbols[i]] = round(data['Close'][len(data)-1],2)
        Change[symbols[i]] = round(((Open[symbols[i]] - previousDayData['Adj Close'][0])/previousDayData['Adj Close'][0])*100,2)
    except:
        print("error extracting symbol %s" % (symbols[i]))
all_stock_data = all_stock_data.sort_values(by='dateTime')
all_stock_data['dateTime'] = all_stock_data['dateTime'].apply(strptime_with_offset)
all_stock_data.rename(columns = {'dateTime':'Symbol'}, inplace=True)
all_stock_data.set_index("Symbol", inplace = True)
all_stock_data = all_stock_data.transpose()
all_stock_data.insert(0, 'Open', Open)
all_stock_data.insert(1, 'Change', Change)
all_stock_data.insert(2, 'LTP', LTP)
all_stock_data.insert(3, 'Totals', Total)
all_stock_data.reset_index(drop=False, inplace=True)
all_stock_data.rename(columns = {'index':'Symbol'}, inplace=True)
all_stock_data = all_stock_data.sort_values(by='Totals', ascending=False)
# all_stock_data = pd.concat([all_stock_data.loc[all_stock_data['LTP'] < 201], all_stock_data.loc[all_stock_data['LTP'] >= 201]])
all_stock_data = all_stock_data.loc[all_stock_data['Open'].notnull()]
all_stock_data['Symbol'] = all_stock_data['Symbol'].str.replace(".NS", "")

try:
    os.mkdir('D:\\Stocks\\{}'.format(today))
except OSError as error:
    print(error)

path = "D:\\Stocks\\" + str(today) + "\\stocks_Interval_" + d.interval + ".xlsx"
all_stock_data.to_excel(path, index=False)