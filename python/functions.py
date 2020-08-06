import time # timing functions
import pandas as pd # data analaysis 
from bs4 import BeautifulSoup # used for web scraping
from selenium import webdriver # creates automated browser
from more_itertools import divide # used for spliting product likes list into equal parts
from selenium.webdriver.common.keys import Keys # used for pressing enter on login screen

# path to chromedriver
# driver = webdriver.Chrome(r'C:\Users\admin\Anaconda3\Lib\site-packages\chromedriver\chromedriver.exe')

def get_driver(login_on = True): # return driver with no images
    options = webdriver.ChromeOptions() # create option
    prefs = {"profile.managed_default_content_settings.images": 2} # preference to disable images
    options.add_experimental_option("prefs", prefs) # add option
    driver = webdriver.Chrome(options=options) # add option o webdriver
    driver = login(driver) if login_on else driver # login diver
    return driver # return driver

def login(driver):  # function for logging in driver
    # login
    username = 'tmebatson@gmail.com'
    password = 'hRIcV' # use getpass in production

    driver.get(r'https://www.wonatrading.com/') # load hompage first so that it picks up cookies
    driver.get(r'https://www.wonatrading.com/login')  # wona login page

    username_textbox = driver.find_element_by_name('email_address')  # find element for email input
    username_textbox.send_keys(username)  # send what you put as userinput

    password_textbox = driver.find_element_by_name('password')  # find element for password input
    password_textbox.send_keys(password)  # send what you put as password
    password_textbox.send_keys(Keys.ENTER) # press enter key after typing password

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

    product_links = []  # this is product urls for all the products on the first page'

    driver.get(product_page)  # first product page

    soup = BeautifulSoup(driver.page_source, 'html5lib')  # soup = parsed html

    # this html element contains the href for the product
    products = soup.find_all('a', style="position:relative;float:left;")

    for product in products:  # iterate each product on webpage
        product_link = product['href']  # assign href to a variable
        product_link = product_link.replace('\r\n', '')  # remove hidden characters from href
        domain = r'https://www.wonatrading.com/' # variable for domain
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

def scrape_product_links(update = False): # use update = True to update data in product_category_urls.csv

    product_links = split_product_links(update)[0][0:1] # links from section 1
    
    scraped_product_links = [] # list of each product scraped
    
    driver_1 = get_driver() # first driver object

    for product_link in product_links:
        print(product_link) # print current product link
        pages = get_product_links(product_link, driver_1)[0:1] # links for all the products on given page
        df = get_data(pages, driver_1) # dataframe = return of function that scrapes data
        scraped_product_links.append(df)  # add df to list

    driver_1.close()  # shut driver off
        
    output_df = pd.concat(scraped_product_links) # combine list into 1 dataframe
    output_df.reset_index(drop=True, inplace=True) # reset index
        
    return output_df # return dataframe

def split_product_links(update = False):
    product_links = get_product_links_data(update)
    page_indexs = divide(4, product_links) # divides list into 4 equal-ish parts
    split_list = [list(page_index) for page_index in page_indexs] # creates a list of 4 lists
    return split_list  # return list
    
def get_pages_data(update = False):

    if not update: # if update is false
        df = pd.read_csv('../csv/product_category_urls.csv').fillna('') # read csv file containing webscraper output
        return df # return lastest csv file
    
    else:  # if update is true, proceed with rest of function
    
        driver = get_driver(login_on=False) # driver does not need to login unless scraping price

        def get_pages(driver):

            pages = {}  # dictionary containing page numbers for each category

            def get_categories(driver):
                # page that shows categories of jewelry
                url = r'https://www.wonatrading.com/jewelry'
                class_ = 'category brrem'  # class of html that contains each category

                # scrape hrefs
                driver.get(url)  # open given url
                soup = BeautifulSoup(driver.page_source, 'html5lib') # soup = parsed html
                html_elements = soup.find_all('a', class_=class_) # html element holding page numbers
                hrefs_list = [page['href'] for page in html_elements] # list of links for each category

                return hrefs_list

            number_of_products_list = []  # this is a list of number of products for each category

            for category in get_categories(driver):

                driver.get(category)

                # text of element containing # of products converted to an int
                number_of_products = int(driver.find_element_by_xpath(
                    '/html/body/div[1]/div/table[2]/tbody/tr/td[3]/table/tbody/tr/td[1]/table/tbody/tr[4]/td/form/table[2]/tbody/tr[4]/td/center/b[3]').text)

                number_of_products_list.append(number_of_products) # add number of products to list

                def get_number_of_products(number_of_products):

                    products_per_page = 100  # the number of products displayed on each page

                    # divmod returns the # of whole pages and the remainder
                    number_of_pages, remainder = divmod(
                        number_of_products, products_per_page)

                    if number_of_pages == 0:  # if there are 0 pages
                        number_of_pages = 1  # 1 is the lowest amount of pages possible
                    else:  # if page > 0
                        if remainder > 0:  # if remainder exsists
                            number_of_pages += 1  # add a page

                    return number_of_pages

                number_of_products = get_number_of_products(number_of_products)

                pages[f'{category}'] = number_of_products

            # return pages dictionary and list for number of products
            return pages, number_of_products_list

        pages, number_of_products_list = get_pages(driver)  # function returns dictionary {'category' : # of products,}

        data = list(pages.items())  # data for dataframe
        columns = ['url', '# of Pages']  # names of columns for dataframe
        df = pd.DataFrame(data=data, columns=columns)  # create dataframe
        # add a column for the number of products per category
        df['# of Products'] = number_of_products_list

        def clean_category(input_string):
            element = 'https://www.wonatrading.com/jewelry/'  # items to remove
            input_string = input_string.replace(
                element, '')  # remove each item
            return input_string.strip()  # return cleaned input string

        # remove https://www.wonatrading.com/jewelry/
        df['Product Category'] = df['url'].apply(clean_category)
        # sort dataframe by least to greatest # of pages
        df.sort_values('# of Pages', inplace=True)
        df.reset_index(drop=True, inplace=True)  # reset index

        driver.close()  # shut driver off

        # write data to csv
        df.to_csv('../csv/product_category_urls.csv', index=False)

        return df

# when update = False product_category_urls.csv is returned
def get_product_links_data(update = False): # this gets every product page

    df = get_pages_data(update) # this returns a dataframe with columns: url, # of Pages, Product Category

    urls_list = []

    for category_index in df.index.tolist():    

        url = df.at[category_index, 'url']

        number_of_pages = df.at[category_index, '# of Pages']

        def get_page_urls(url, number_of_pages): # this function gets urls for every page # 
            page_urls = [] # list containing urls for each page number
            for i in range(number_of_pages): # for each page number
                if i == 0: # if the index is 0
                    page_urls.append(url) # the main page is first page
                else: # any number highier than that
                    i += 1 # add 1 to index
                    page_urls.append(f'{url}/page={i}') # add page number to url
            return page_urls # return filled list

        result = get_page_urls(url, number_of_pages)

        urls_list.extend(result)

    return urls_list

# # exec(open('./python/sample.py').read()) # open python file in shell
