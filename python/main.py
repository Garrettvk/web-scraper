import pandas as pd
from functions import *

pd.set_option('display.max_colwidth', None) # prints entire column width
pd.set_option('display.max_columns', None) # show all columns and rows
pd.set_option('display.max_rows', None)

pages = get_product_links()[0:2] # first 2 pages
df = get_data(pages) # dataframe from get_data function
df