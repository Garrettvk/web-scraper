import pandas as pd

df = pd.read_csv('csv/24541 products.csv').fillna('')  # open csv as dataframe


class Stock:

    def __init__(self, name, price, category):

        self.name = name
        self.price = price
        self.category = category


names = df['Product Name'].values.tolist()
prices = df['Cost Price'].values.tolist()
category = df['Category'].values.tolist()

objects = [Stock(name, price, category) for name, price, category in zip(names, prices, category)]
