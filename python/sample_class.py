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
        start = self.url.rindex('/') + 1
        return self.url[start:]

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
            if remainder > 0:  # if remainder exsists
                number_of_pages += 1  # add a page

        return number_of_pages        

    def get_page_urls(self):
        return [self.url + f'/page={i}' for i in range(2, self.page_count + 1)]

    def get_product_urls(self):
        product_links = []  # this is product urls for all the products on the first page'

        driver.get(self.url)  # first product page

        soup = BeautifulSoup(driver.page_source, 'html5lib')  # parsed html

        # this html element contains the href for the product
        products = soup.find_all('a', style="position:relative;float:left;")

        for product in products:  # iterate each product on webpage
            product_link = product['href']  # assign href to a variable
            product_link = product_link.replace('\r\n', '')  # remove hidden characters from href
            domain = r'https://www.wonatrading.com/' # variable for domain
            product_links.append(f'{domain}{product_link}')  # add domain
                
        return product_links


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


for page in category_pages:
    output = Page(page)
    print(output.product_urls)


# exec(open('./python/sample_class.py').read()) # open python file in shell
