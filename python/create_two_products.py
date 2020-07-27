import pandas as pd
from scrape_one_product import *

# prints entire column width
pd.set_option('display.max_colwidth', 1000)

# show all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# currently these html files are strings that represent a file name
# the with open function uses these variables to open local html files
# in production these strings should contain the urls for each product page
# rather than opening a local html file, 
# the requests library should parse product pages on wonatrading.com
pages = ['simple.html', 'simple2.html'] # variable for html pages

df = scrape_data(pages) # dataframe from scrape_data function

df.to_csv('output.csv', index = False) # write dataframe to csv

print(df) # print df