import time  # timing functions
import pandas as pd  # data analaysis
from bs4 import BeautifulSoup  # used for web scraping
from selenium import webdriver  # creates automated browser
# used for spliting product likes list into equal parts
from more_itertools import divide
# used for pressing enter on login screen
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

class Page:

    domain = 'https://www.wonatrading.com/'

    def __init__(self, url):
        self.url = url
        self.category = self.get_category()
        self.count = self.get_product_count()

    def get_category(self):
        start = self.url.rindex('/') + 1
        return self.url[start:]

    def get_product_count(self):
        driver.get(self.url)
        # text of element containing # of products converted to an int
        return int(driver.find_element_by_xpath('/html/body/div[1]/div/table[2]/tbody/tr/td[3]/table/tbody/tr/td[1]/table/tbody/tr[4]/td/form/table[2]/tbody/tr[4]/td/center/b[3]').text)

    # def category_urls(self):
    #     driver.get(self.url)  # open given url
    #     # soup = parsed html
    #     soup = BeautifulSoup(driver.page_source, 'html5lib')
    #     # html element holding page numbers
    #     html_elements = soup.find_all(self.tag, class_=self.class_)
    #     # list of links for each category
    #     return [page['href'] for page in html_elements]

anklet_page = Page(f'{Page.domain}jewelry/anklet')


# jewelry_page = Page('https://www.wonatrading.com/jewelry',
#                     'category brrem', 'a')

category_pages = [
    'https://www.wonatrading.com/jewelry/anklet', 
    'https://www.wonatrading.com/jewelry/bracelet', 
    'https://www.wonatrading.com/jewelry/brooch', 
    'https://www.wonatrading.com/jewelry/body-jewelry', 
    'https://www.wonatrading.com/jewelry/cubic-zirconia', 
    'https://www.wonatrading.com/jewelry/earring',
    'https://www.wonatrading.com/jewelry/mask', 
    'https://www.wonatrading.com/jewelry/necklace', 
    'https://www.wonatrading.com/jewelry/pendant-set', 
    'https://www.wonatrading.com/jewelry/ring', 
    'https://www.wonatrading.com/jewelry/stainless-steel', 
    'https://www.wonatrading.com/jewelry/watch', 
    'https://www.wonatrading.com/jewelry/jewelry-component', 
    'https://www.wonatrading.com/jewelry/jewelry-display']

for page in category_pages:
    output = Page(page)
    print(output.count)


# class Product:

#     def __init__(self, xpath):
#         self.xpath = xpath

#     def get_product_count(self):
#         product_count_list = []  # this is a list of number of products for each category

#         for category in Page.category_urls():

#             driver.get(category)  # open page

#             # text of element containing # of products converted to an int
#             number_of_products = int(
#                 driver.find_element_by_xpath(self.xpath).text)

#             # add number of products to list
#             product_count_list.append(number_of_products)

#             return product_count_list


# product_1 = Product(
#     '/html/body/div[1]/div/table[2]/tbody/tr/td[3]/table/tbody/tr/td[1]/table/tbody/tr[4]/td/form/table[2]/tbody/tr[4]/td/center/b[3]')


# exec(open('./python/sample_class.py').read()) # open python file in shell
