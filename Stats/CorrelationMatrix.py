import pandas as pd

data = pd.read_excel(
    'D:\\Stocks\\2020-12-31\\stocks_2020-12-31.xlsx')

# transposedData = data.iloc[:, 5:].T
# df = transposedData.rename(columns=data.Symbol)
# print(df)
# df = pd.DataFrame(data.iloc[:, 3:].T, columns=data.Symbol)
# print(df.head)

corrMatrix = pd.DataFrame.corr(data)
corrMatrix.to_csv('C:\\Users\\chlsp\\Desktop\\correlationStocks1.csv')
