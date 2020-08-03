from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# path to chromedriver
# driver = webdriver.Chrome(r'C:\Users\admin\Anaconda3\Lib\site-packages\chromedriver\chromedriver.exe')

def get_driver(): # functioin returns a drive with no images
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

def get_product_links(product_page, driver):

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

    password_textbox.send_keys(Keys.ENTER) # press enter key after typing password

    product_links = []  # this is product urls for all the products on the first page'

    driver.get(product_page)  # first product page

    soup = BeautifulSoup(driver.page_source, 'html5lib')  # soup = parsed html

    # this html element contains the href for the product
    products = soup.find_all('a', style="position:relative;float:left;")

    for product in products:  # iterate each product on webpage
        product_link = product['href']  # assign href to a variable
        product_link = product_link.replace('\r\n', '')  # remove hidden characters from href
        product_links.append(f'{domain}{product_link}')  # add domain
            
    return product_links

def scrape_data(product_page_url, driver):  # gets data from single page

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

def get_data(pages, driver): # iterate over pages and create dataframe

    data = []  # list of data from each page

    # column names are from webscrapper output
    columns = ['Product Name', 'Category', 'Product Image File - 1', 'Product Image File - 2', 'Product Description', 'Cost Price']

    try: # try while ip isn't blocked
        for page in pages:  # iterate over html for each product
            time.sleep(10) # sleep function limits the number of requests over time
            page = scrape_data(page, driver) # page = return of scrape_data function
            data.append(page)  # add data from page

    except AttributeError:      

        # create dataframe
        df = pd.DataFrame(columns=columns, data=data)

        return df    

    # create dataframe
    df = pd.DataFrame(columns=columns, data=data)

    return df
