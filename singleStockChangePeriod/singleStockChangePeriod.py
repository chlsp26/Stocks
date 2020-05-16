import yfinance as yf
import pandas as pd
from datetime import timedelta
from datetime import datetime
from datetime import date
import data as d
import numpy as np

dates = pd.read_excel('C:\\Users\\chlsp\\Desktop\\Python\\Dates.xlsx')

today = date.today()

def calculate_PL_percentage(data):
    percentages = pd.DataFrame({'dateTime':[], 'percentage': []})
    data['Datetime'] = data['Datetime'].apply(strftime_with_offset)
    for i in data.index:
        if i == 0:
            percentages = percentages.append({'dateTime': data['Datetime'][i], 'percentage': round(((data['Close'][i] - data['Open'][i])/data['Open'][i])*100,2)}, ignore_index=True)
        else:
            percentages = percentages.append({'dateTime': data['Datetime'][i], 'percentage': round(((data['Close'][i] - data['Close'][i-1])/data['Close'][i-1])*100,2)}, ignore_index=True)
    return percentages

def strftime_with_offset(date, format='%H:%M:%S'):
    base_dt = datetime.strftime(date, format)
    return base_dt

def strfdate_with_offset(date, format='%Y-%m-%d'):
    base_dt = datetime.strftime(date, format)
    return base_dt

stockmarketdates = pd.Series([])
for i in dates.Date.index:
    stockmarketdates[i] = strfdate_with_offset(dates.Date[i])


all_stock_data = pd.DataFrame()
LTP = pd.Series([])
Open = pd.Series([])
Total = pd.Series([])
Change = pd.Series([])
for i in stockmarketdates.index:
    try:
        stock = yf.Ticker(d.ticker + ".NS")
        data = stock.history(interval=d.interval, start=stockmarketdates[i], end=stockmarketdates[i+1])
        data.dropna(how='all',inplace=True)
        print("%d out of %d completed" % (i+1, len(stockmarketdates)))
        data.reset_index(drop=False, inplace=True)
        if len(all_stock_data) == 0:
            all_stock_data = calculate_PL_percentage(data)
            all_stock_data.rename(columns = {'percentage':stockmarketdates[i]}, inplace=True)
        else:
            all_stock_data = pd.merge(all_stock_data, calculate_PL_percentage(data), how='outer', on='dateTime')
            all_stock_data.rename(columns = {'percentage':stockmarketdates[i]}, inplace=True)
        Total[stockmarketdates[i]] = all_stock_data[stockmarketdates[i]].sum()
        Open[stockmarketdates[i]] = round(data['Open'][0],2)
        LTP[stockmarketdates[i]] = round(data['Close'][len(data)-1],2)
    except:
        print("error extracting date %s" % (stockmarketdates[i]))

all_stock_data = all_stock_data.sort_values(by='dateTime')
all_stock_data.rename(columns = {'dateTime':'Date'}, inplace=True)
all_stock_data.set_index("Date", inplace = True)
all_stock_data = all_stock_data.transpose()
all_stock_data.insert(0, 'Open', Open)
all_stock_data.insert(1, 'LTP', LTP)
all_stock_data.insert(2, 'Totals', Total)
all_stock_data.reset_index(drop=False, inplace=True)
all_stock_data.rename(columns = {'index':'Date'}, inplace=True)
all_stock_data = all_stock_data.sort_values(by='Date', ascending=False)
all_stock_data.dropna(how='all', axis=1,inplace=True)

for i in range(len(all_stock_data.Date)-1,-1,-1):
    if i == 0:
        Change[all_stock_data.Date[i]] = np.nan
    else:
        Change[all_stock_data.Date[i]] = round(((all_stock_data['Open'][i] - all_stock_data['LTP'][i-1])/all_stock_data['LTP'][i-1])*100,2)
all_stock_data.set_index("Date", inplace = True)
all_stock_data.insert(3, 'Change', Change)
all_stock_data.reset_index(drop=False, inplace=True)

path = "D:\\Stocks\\" + str(today) + "\\" + d.ticker + "_Interval.xlsx"
all_stock_data.to_excel(path, index=False)