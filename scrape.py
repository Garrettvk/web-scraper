from bs4 import BeautifulSoup
import requests

with open('simple.html') as html_file: # open html file
    soup = BeautifulSoup(html_file, 'lxml') # soup = parsed html

# print product names
for product_name in soup.find_all('font', style = 'display: block;height:40px;text-transform: uppercase;'):
    print(product_name.text)