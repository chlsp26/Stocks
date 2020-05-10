import yfinance as yf
import pandas as pd
from datetime import timedelta
from datetime import datetime
from datetime import date

tickers = pd.read_csv('C:\\Users\\chlsp\\Desktop\\Python\\EQUITY_L.csv')
extension = 'NS'
symbols = tickers.SYMBOL + '.' + 'NS'

def calculate_PL_percentage(data):
    percentages = pd.DataFrame({'date':[], 'percentage': []})
    for i in data.index:
        if i == 0:
            percentages = percentages.append({'date': data['Date'][i], 'percentage': 0}, ignore_index=True)
        else:
            percentages = percentages.append({'date': data['Date'][i], 'percentage': round(((data['Adj Close'][i] - data['Adj Close'][i-1])/data['Adj Close'][i-1])*100,2)}, ignore_index=True)
    return percentages

def strptime_with_offset(date, format='%d-%m-%Y'):
            base_dt = datetime.strftime(date, format)
            return base_dt

all_stock_data = pd.DataFrame()
LTP = pd.Series([])
Total = pd.Series([])
for i in range(0,2,1):
    try:
        data = yf.download(symbols[i], start="2020-02-28", end="2020-05-30")
        data.dropna(how='all',inplace=True)
        print("%d out of %d completed" % (i+1, len(symbols)))
        data.reset_index(drop=False, inplace=True)
        if len(all_stock_data) == 0:
            all_stock_data = calculate_PL_percentage(data)
            all_stock_data.rename(columns = {'percentage':symbols[i]}, inplace=True)
        else:
            all_stock_data = pd.merge(all_stock_data, calculate_PL_percentage(data), how='outer', on='date')
            all_stock_data.rename(columns = {'percentage':symbols[i]}, inplace=True)
        Total[symbols[i]] = all_stock_data[symbols[i]].sum()
        LTP[symbols[i]] = round(data['Adj Close'][len(data)-1],2)
    except:
        print("error extracting symbol %s" % (symbols[i]))
all_stock_data = all_stock_data.sort_values(by='date', ascending=False)
all_stock_data['date'] = all_stock_data['date'].apply(strptime_with_offset)
all_stock_data.rename(columns = {'date':'Symbol'}, inplace=True)
all_stock_data.set_index("Symbol", inplace = True)
all_stock_data = all_stock_data.transpose()
all_stock_data.insert(0, 'LTP', LTP)
all_stock_data.insert(1, 'Totals', Total)
all_stock_data.reset_index(drop=False, inplace=True)
all_stock_data.rename(columns = {'index':'Symbol'}, inplace=True)
all_stock_data = all_stock_data.iloc[:,:-1]
all_stock_data = all_stock_data.sort_values(by='Totals', ascending=False)
all_stock_data = pd.concat([all_stock_data.loc[all_stock_data['LTP'] < 201], all_stock_data.loc[all_stock_data['LTP'] >= 201]])
all_stock_data = all_stock_data.loc[all_stock_data['Totals'] != 0]
all_stock_data['Symbol'] = all_stock_data['Symbol'].str.replace(".NS", "")

today = date.today()
path = "D:\\Stocks\\" + str(today) + "\\stocks_{0}.xlsx".format(today)
all_stock_data.to_excel(path, index=False)