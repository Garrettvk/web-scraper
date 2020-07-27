from bs4 import BeautifulSoup
import requests
import pandas as pd
from clean_description import *

def scrape_one_product(html):
        

    with open(f'../html/{html}') as html_file:  # open html file
        soup = BeautifulSoup(html_file, 'lxml')  # soup = parsed html

    product_name = soup.find('h2').text

    categories = soup.find_all('a', style='font-family:eurof;font-size:14px;')

    category1, category2, category3 = categories[0].text, categories[1].text, categories[2].text

    image1 = soup.find('img', id='main_img')['src']

    image2 = soup.find('img', id='des_img')['src']

    # raw description
    description = soup.find('td', class_='tdBorder').find('p').text

    # clean description
    description = clean_description(description)

    # raw price
    price = soup.find('td', class_='products_info_price').text

    # cleaned price
    price = clean_price(price)

    # each product attribute is put into a list
    data = [product_name, category1, category2,
            category3, image1, image2, description, price]    

    return data

def scrape_data(pages):
    
    data = [] # list of data from each page

    for page in pages: # iterate over html for each product
        page = scrape_one_product(page) # page = return of scrape_one_product function
        data.append(page) # add data from page

    # column names are from webscrapper output
    columns = ['productname', 'category1', 'category2',
            'category3', 'image1', 'image2', 'description', 'price']

    # create dataframe
    df = pd.DataFrame(columns = columns, data = data)

    return df