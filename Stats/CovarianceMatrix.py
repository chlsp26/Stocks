import pandas as pd

data = pd.read_excel(
    'D:\\Stocks\\2020-10-26\\finalstocks_2020-10-26_08-56-45.530469.xlsx')

transposedData = data.iloc[:, 3:].T
df = transposedData.rename(columns=data.Symbol)
print(df)
# df = pd.DataFrame(data.iloc[:, 3:].T, columns=data.Symbol)
# print(df.head)

covMatrix = pd.DataFrame.cov(df)
covMatrix.to_csv('C:\\Users\\chlsp\\Desktop\\comprisionStocks.csv')
