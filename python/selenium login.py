from selenium import webdriver
from bs4 import BeautifulSoup

# path to chromedriver
driver = webdriver.Chrome(r'C:\Users\admin\Anaconda3\Lib\site-packages\chromedriver\chromedriver.exe')

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

for category in get_categories():

    driver.get(category)

    number_of_products = int(driver.find_element_by_xpath('//*[@id="buyForm"]/table[2]/tbody/tr[4]/td/center/b[3]').text)


    number_of_pages = (number_of_products // 100) + 1
    
    print(number_of_pages)

