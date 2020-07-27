import pandas as pd
from scrape_one_product import scrape_one_product

# variable for html page
pages = ['simple.html', 'simple2.html']

# create dataframe from return of function
data = []

for page in pages:
    page = scrape_one_product(page)
    data.append(page)

# column name is from webscrapper output
columns = ['productname', 'category1', 'category2',
        'category3', 'image1', 'image2', 'description', 'price']

# create dataframe, notice that data list is wrapped in brackets
df = pd.DataFrame(columns = columns, data = data)

# write dataframe to csv
df.to_csv('output.csv', index = False)