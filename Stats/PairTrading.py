import pandas as pd

# stockPairs = pd.read_csv('D:\\Stocks\\StockPairs.csv')
stockPrices = pd.read_excel('D:\\Stocks\\2020-12-31\\stocks_2020-12-31.xlsx')
correlation_mat = pd.DataFrame.corr(stockPrices)
corr_pairs = correlation_mat.unstack()
sorted_pairs = corr_pairs.sort_values(kind="quicksort")
pairs = sorted_pairs[sorted_pairs != 1]
strong_pairs = pairs[pairs > 0.97]
print(strong_pairs.index[0][0])

for i in strong_pairs.index:
    stockA = stockPrices[strong_pairs.index[i][0]]
    stockB = stockPrices[strong_pairs.index[i][1]]
    ratio = stockA/stockB
    print(ratio)
