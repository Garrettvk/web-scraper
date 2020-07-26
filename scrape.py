from bs4 import BeautifulSoup
import requests

url = 'https://www.wonatrading.com/jewelry/anklet'

with open('simple.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

for product_name in soup.find_all('font', style = 'display: block;height:40px;text-transform: uppercase;'):
    print(product_name.text)