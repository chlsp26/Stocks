import yfinance as yf
import data as d
# stock = yf.Ticker("CIPLA.NS")
# data = stock.history(period="1d", interval='10m')
# print(data)
# print(d)
previousDayData = yf.download(
    "EQUITAS.NS", start="2020-10-12", end="2020-12-30")
print(previousDayData)


# data = stock.history(interval='1d',
#                      start='2020-10-01', end='2020-11-18')
# data.to_csv("cipla.csv")

# print(data)
