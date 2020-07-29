import pandas as pd
from scrape_one_product import *

# prints entire column width
pd.set_option('display.max_colwidth', 1000)

# show all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

pages = get_product_links()[0:2] # first 2 pages

df = scrape_data(pages) # dataframe from scrape_data function

df.to_csv('output.csv', index = False) # write dataframe to csv

print(df) # print df