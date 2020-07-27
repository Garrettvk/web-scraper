from bs4 import BeautifulSoup
import requests
import pandas as pd


product_links = [] # this is product urls for all the products on the first page

with open('html/Products Page.html') as html_file:  # open html file
        soup = BeautifulSoup(html_file, 'lxml')  # soup = parsed html

        # this html element contains the href for the product
        products = soup.find_all('a', style="position:relative;float:left;")

        # since the href doesn't have the domain included, we need to add it 
        domain = 'https://www.wonatrading.com/'

        for product in products: # iterate of each product on webpage
            product_link = product['href']  # product_link = this href
            product_link = product_link.replace('\n', '') # remove newline characters from product link
            product_links.append(f'{domain}{product_link}') # combine the domain and product_link

for product_link in product_links:
    print(product_link)

