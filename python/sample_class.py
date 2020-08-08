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
        self.page_count = self.get_product_pages()
        self.page_urls = self.get_page_urls()
        self.product_urls = self.get_product_urls()

    def get_category(self):
        start = self.url.rindex('/') + 1 # string of category starts at the last /
        return self.url[start:] # slice string

    def get_product_count(self):
        driver.get(self.url)
        # text of element containing # of products converted to an int
        return int(driver.find_element_by_xpath('/html/body/div[1]/div/table[2]/tbody/tr/td[3]/table/tbody/tr/td[1]/table/tbody/tr[4]/td/form/table[2]/tbody/tr[4]/td/center/b[3]').text)

    def get_product_pages(self):
        products_per_page = 100  # the number of products displayed on each page

        # divmod returns the # of whole pages and the remainder
        number_of_pages, remainder = divmod(
            self.count, products_per_page)

        if number_of_pages == 0:  # if there are 0 pages
            number_of_pages = 1  # 1 is the lowest amount of pages possible
        else:  # if page > 0
            if remainder > 0:  # if remainder exists
                number_of_pages += 1  # add a page

        return number_of_pages        

    def get_page_urls(self):
        return [self.url + f'/page={i}' for i in range(2, self.page_count + 1)]

    def get_product_urls(self):
        product_links = []  # list for product links that will be returned

        first_page = [self.url] # first page for iterating products
        product_pages = self.get_page_urls() # every other page after the first
        product_pages = first_page + product_pages # add first page to complete set

        for product_page in product_pages: # for every page containing products
            driver.get(product_page)  # open product_page in selenium
            soup = BeautifulSoup(driver.page_source, 'html5lib')  # parse html

            # html element for href of each product
            products = soup.find_all('a', style="position:relative;float:left;")

            for product in products:  # iterate each product on webpage
                product_link = product['href']  # assign href to a variable
                product_link = product_link.replace('\r\n', '')  # remove hidden characters from href
                product_links.append(f'{Page.domain}{product_link}') # add domain
                
        return product_links # return product links found

all_products = []

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
    'https://www.wonatrading.com/jewelry/jewelry-display'
    ]

for category in category_pages: # for each category
    Page_object = Page(category) # create a Page Object
    all_products += Page_object.product_urls # add all product links to all products list
     

# 32983 products found!
print(len(all_products))


# exec(open('./python/sample_class.py').read()) # open python file in shell
