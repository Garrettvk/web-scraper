from selenium import webdriver
from bs4 import BeautifulSoup
import pprint


# path to chromedriver
# driver = webdriver.Chrome(r'C:\Users\admin\Anaconda3\Lib\site-packages\chromedriver\chromedriver.exe')

# remove images
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

def scrape_hrefs(url, class_):
    driver.get(url) # open given url
    soup = BeautifulSoup(driver.page_source, 'html5lib')  # soup = parsed html
    html_elements = soup.find_all('a', class_ = class_) # html element holding page numbers
    hrefs_list = [page['href'] for page in html_elements]  # list of links for each category    
    return hrefs_list # return list of hrefs

def get_page_numbers(url):  # function the gets url for product pages
    class_ = 'pageResults' # class of html that contains each category    
    page_urls_list = scrape_hrefs(url, class_) # get hrefs for each product page
    page_urls_list.insert(0, driver.current_url) # add the url of first product page to beginning of list

    # Create a dictionary, using the List items as keys.
    # This will automatically remove any duplicates because dictionaries cannot have duplicate keys.
    page_urls_list = list(dict.fromkeys(page_urls_list))  # remove duplicates

    return page_urls_list # return list of urls

def get_categories():
    url = r'https://www.wonatrading.com/jewelry' # page that shows categories of jewelry
    class_ = 'category brrem' # class of html that contains each category
    category_hrefs = scrape_hrefs(url, class_)  # list of all the hrefs for wach category
    return category_hrefs

def get_all_products():

    all_products = [] # list for href of every product category and its pages
    category_hrefs = get_categories() # get list of hrefs for each category

    for category in category_hrefs: # for each href of category
        product_pages = get_page_numbers(category)  # list of hrefs for each category
        all_products.extend(product_pages)  # extend all_products list with list of hrefs for each category
        
    return all_products

def get_number_of_products(number_of_products):

    products_per_page = 100 # the number of products displayed on each page
    number_of_pages, remainder = divmod(number_of_products, products_per_page)  # divmod returns the # of whole pages and the remainder

    if number_of_pages == 0: # if there are 0 pages
        number_of_pages = 1 # 1 is the lowest amount of pages possible
    else: # if page > 0
        if remainder > 0: # if remainder exsists
            number_of_pages += 1 # add a page

    return number_of_pages

def get_pages(driver):

    pages = {} # dictionary containg page numbers for each category

    for category in get_categories():

        driver.get(category)


        # text of element containing # of products converted to an int
        number_of_products = int(driver.find_element_by_xpath('/html/body/div[1]/div/table[2]/tbody/tr/td[3]/table/tbody/tr/td[1]/table/tbody/tr[4]/td/form/table[2]/tbody/tr[4]/td/center/b[3]').text)
        
        number_of_products = get_number_of_products(number_of_products)
        
        pages[f'{category}'] = number_of_products

    return pages

# exec(open('./python/sample.py').read())

pages = get_pages(driver)

pprint.pprint(pages)