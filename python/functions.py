from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import pprint

# path to chromedriver
# driver = webdriver.Chrome(r'C:\Users\admin\Anaconda3\Lib\site-packages\chromedriver\chromedriver.exe')

# remove images 
def get_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver

def clean_description(input_string):

    remove_list = ['�', '\n', '\t', '•'] # items to remove

    for element in remove_list: # iterate over items in list
        input_string = input_string.replace(element, '') # remove each item

    return input_string.strip() # return cleaned input string

def clean_price(input_string):
    # $4.25 / pc

    remove_list = ['$', '/ pc', '\n',] # items to remove

    for element in remove_list: # iterate over items in list
        input_string = input_string.replace(element, '') # remove each item

    return input_string.strip()

def get_product_links():

    # login
    # turn this off in production, use method up top ^
    username = 'tmebatson@gmail.com'
    password = 'hRIcV'

    domain = r'https://www.wonatrading.com/'

    # load hompage first so that it picks up cookies
    driver.get(domain)
    driver.get(r'https://www.wonatrading.com/login')  # wona login page

    username_textbox = driver.find_element_by_name(
        'email_address')  # find element for email input
    username_textbox.send_keys(username)  # send what you put as userinput

    password_textbox = driver.find_element_by_name(
        'password')  # find element for password input
    password_textbox.send_keys(password)  # send what you put as password

    login_button = driver.find_element_by_id(
        'btnLogin')  # element of login button
    login_button.click()  # clicks login button

    product_links = []  # this is product urls for all the products on the first page

    product_page = r'https://www.wonatrading.com/jewelry/anklet'

    driver.get(product_page)  # first product page

    soup = BeautifulSoup(driver.page_source, 'html5lib')  # soup = parsed html

    # this html element contains the href for the product
    products = soup.find_all('a', style="position:relative;float:left;")

    for product in products:  # iterate each product on webpage
        product_link = product['href']  # assign href to a variable
        product_link = product_link.replace('\r\n', '')  # remove hidden characters from href
        product_links.append(f'{domain}{product_link}')  # add domain
            
    return product_links

def scrape_data(product_page_url):  # gets data from single page

    driver.get(product_page_url)  # open first product page

    soup = BeautifulSoup(driver.page_source, 'lxml')  # soup = parsed html

    product_name = soup.find('h2').text

    categories = soup.find_all(
        'a', style='font-family:eurof;font-size:14px;')

    # combine all 3 categories and seperate with ; and /
    Category = f'{categories[0].text};{categories[1].text}/{categories[2].text}'

    image1 = soup.find('img', id='main_img')['src']

    try:  # try looking for second image
        image2 = soup.find('img', id='des_img')['src']

    except TypeError:  # if there's no image it will raise a type error and stop the program
        image2 = ''  # all we need is an empty string

    # raw description
    description = soup.find('td', class_='tdBorder').find('p').text

    # clean description
    description = clean_description(description)

    # raw price
    price = soup.find('td', class_='products_info_price').text

    # cleaned price
    price = clean_price(price)

    # each product attribute is put into a list
    data = [product_name, Category, image1, image2, description, price]

    return data

def get_data(pages): # iterate over pages and create dataframe

    data = []  # list of data from each page

    # column names are from webscrapper output
    columns = ['Product Name', 'Category', 'Product Image File - 1', 'Product Image File - 2', 'Product Description', 'Cost Price']

    try: # try while ip isn't blocked
        for page in pages:  # iterate over html for each product
            time.sleep(10) # sleep function limits the number of requests over time
            page = scrape_data(page) # page = return of scrape_data function
            data.append(page)  # add data from page

    except AttributeError:      

        # create dataframe
        df = pd.DataFrame(columns=columns, data=data)

        return df    

    # create dataframe
    df = pd.DataFrame(columns=columns, data=data)

    return df

def get_pages_data():

    # use this dictionary for testing, 
    # in productioin pages should = get_pages(driver) that way the page numbers are up to date
    pages = {'https://www.wonatrading.com/jewelry/anklet': 2,      
            'https://www.wonatrading.com/jewelry/body-jewelry': 2,
            'https://www.wonatrading.com/jewelry/bracelet': 85,
            'https://www.wonatrading.com/jewelry/brooch': 7,
            'https://www.wonatrading.com/jewelry/cubic-zirconia': 15,
            'https://www.wonatrading.com/jewelry/earring': 137,
            'https://www.wonatrading.com/jewelry/jewelry-component': 1,
            'https://www.wonatrading.com/jewelry/jewelry-display': 1,
            'https://www.wonatrading.com/jewelry/mask': 4,
            'https://www.wonatrading.com/jewelry/necklace': 73,
            'https://www.wonatrading.com/jewelry/pendant-set': 3,
            'https://www.wonatrading.com/jewelry/ring': 9,
            'https://www.wonatrading.com/jewelry/stainless-steel': 1,
            'https://www.wonatrading.com/jewelry/watch': 1}

    data = list(pages.items()) # data for dataframe
    columns = ['url','# of Pages'] # names of columns for dataframe
    df = pd.DataFrame(data = data, columns = columns) # create dataframe
    
    def clean_category(input_string):
        element = 'https://www.wonatrading.com/jewelry/' # items to remove
        input_string = input_string.replace(element, '') # remove each item
        return input_string.strip() # return cleaned input string

    df['Product Category'] = df['url'].apply(clean_category) # remove https://www.wonatrading.com/jewelry/
    df.sort_values('# of Pages', inplace=True) # sort dataframe by least to greatest # of pages
    df.reset_index(drop=True, inplace=True) # reset index

    return df

def get_number_of_products(number_of_products):

    products_per_page = 100 # the number of products displayed on each page
    number_of_pages, remainder = divmod(number_of_products, products_per_page)  # divmod returns the # of whole pages and the remainder

    if number_of_pages == 0: # if there are 0 pages
        number_of_pages = 1 # 1 is the lowest amount of pages possible
    else: # if page > 0
        if remainder > 0: # if remainder exsists
            number_of_pages += 1 # add a page

    return number_of_pages

def scrape_hrefs(url, class_, driver):
    driver.get(url) # open given url
    soup = BeautifulSoup(driver.page_source, 'html5lib')  # soup = parsed html
    html_elements = soup.find_all('a', class_ = class_) # html element holding page numbers
    hrefs_list = [page['href'] for page in html_elements]  # list of links for each category    
    return hrefs_list # return list of hrefs

def get_categories(driver):
    url = r'https://www.wonatrading.com/jewelry' # page that shows categories of jewelry
    class_ = 'category brrem' # class of html that contains each category
    category_hrefs = scrape_hrefs(url, class_, driver)  # list of all the hrefs for wach category
    return category_hrefs

def get_pages(driver):

    pages = {} # dictionary containg page numbers for each category

    for category in get_categories(driver):

        driver.get(category)


        # text of element containing # of products converted to an int
        number_of_products = int(driver.find_element_by_xpath('/html/body/div[1]/div/table[2]/tbody/tr/td[3]/table/tbody/tr/td[1]/table/tbody/tr[4]/td/form/table[2]/tbody/tr[4]/td/center/b[3]').text)
        
        number_of_products = get_number_of_products(number_of_products)
        
        pages[f'{category}'] = number_of_products

    return pages

def get_page_urls(url, number_of_pages): # this function gets urls for every page # 
    page_urls = [] # list containg urls for each page number
    for i in range(number_of_pages): # for each page number
        if i == 0: # if the index is 0
            page_urls.append(url) # the main page is first page
        else: # any number highier than that
            i += 1 # add 1 to index
            page_urls.append(f'{url}/page={i}') # add page number to url
    return page_urls # return filled list

# exec(open('./python/sample.py').read())

# for printing pages dictionary
# driver = get_driver()
# pages = get_pages(driver)
# pprint.pprint(pages)