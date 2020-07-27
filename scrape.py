from bs4 import BeautifulSoup
import requests

with open('simple.html') as html_file: # open html file
    soup = BeautifulSoup(html_file, 'lxml') # soup = parsed html

product_names = []

# print product names
for product_name in soup.find_all('font', style = 'display: block;height:40px;text-transform: uppercase;'):
    product_names.append(product_name.text)

# finds categories but doesn't find fashion
# fashion is found when you click on the item
# for product_name in soup.find_all('a', style = 'font-family:eurof;font-size:14px;'):
#     print(product_name.text)

# prints image links
for title in product_names:

    for product_name in soup.find_all('img', title = title):

        domain = 'https://www.wonatrading.com/'
        image_link = product_name['src']
        output = domain + image_link
        print(output)