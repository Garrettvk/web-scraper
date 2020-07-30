from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

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

    product_links = []  # this is product urls for all the products on the first page

    products_url = 'https://www.wonatrading.com/jewelry/anklet'  # url for login page
    # second_page = 'https://www.wonatrading.com/jewelry/anklet/page=2'
    domain = 'https://www.wonatrading.com/' # domain of website

    headers = {
        'cookie' : 'cookie_test=please_accept_for_session; __auc=8afe36de17389481e509d9e1c71; _ga=GA1.2.1781461277.1595736073; __tawkuuid=e::wonatrading.com::fl9A0cET/otx3JZxKB32n8j9xbPsMZQihfmL3WpUIh9u8t5UPxjwBuOSWYmVuhza::2; __adroll_fpc=76b3cd1ee25f0f80997d6c6b0f53fd86-1595736074261; _fbp=fb.1.1595736074767.210364020; _gid=GA1.2.1153286955.1595996477; osCsid=o9t4vidjg18hblbpoj8h93chc1; __asc=4c7656061739a9974840637ce99; _gat_gtag_UA_46005179_1=1; TawkConnectionTime=0; __ar_v4=G3NB2AWGMJALLM3LQB7B6W%3A20200725%3A66%7CYCTJCPNBHJAIPIVE526GC4%3A20200725%3A66%7CLM3XUYFU3ZECHJECYX2EJI%3A20200725%3A66',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    }

    with requests.Session() as session:  # open html file    
        
        request = session.get(products_url, headers=headers).content # request products page
        soup = BeautifulSoup(request, 'html5lib')  # soup = parsed html

        # this html element contains the href for the product
        products = soup.find_all('a', style="position:relative;float:left;")

        for product in products:  # iterate each product on webpage
            product_link = product['href']  # assign href to a variable
            product_link = product_link.replace('\r\n', '')  # remove hidden characters from href
            product_links.append(f'{domain}{product_link}')  # add domain
            
    return product_links

def scrape_data(product_page_url): # gets data from single page

    headers = {
        'cookie': 'cookie_test=please_accept_for_session; __auc=8afe36de17389481e509d9e1c71; _ga=GA1.2.1781461277.1595736073; __tawkuuid=e::wonatrading.com::fl9A0cET/otx3JZxKB32n8j9xbPsMZQihfmL3WpUIh9u8t5UPxjwBuOSWYmVuhza::2; __adroll_fpc=76b3cd1ee25f0f80997d6c6b0f53fd86-1595736074261; _fbp=fb.1.1595736074767.210364020; osCsid=lcau16rhuad4cgo3nqt1g6k103; __asc=e88cdaa517398cd92b44cd05553; _gid=GA1.2.1153286955.1595996477; _gat_gtag_UA_46005179_1=1; TawkConnectionTime=0; __ar_v4=G3NB2AWGMJALLM3LQB7B6W%3A20200725%3A52%7CYCTJCPNBHJAIPIVE526GC4%3A20200725%3A52%7CLM3XUYFU3ZECHJECYX2EJI%3A20200725%3A52',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }

    product_headers = {
        'cookie': 'cookie_test=please_accept_for_session; __auc=8afe36de17389481e509d9e1c71; _ga=GA1.2.1781461277.1595736073; __tawkuuid=e::wonatrading.com::fl9A0cET/otx3JZxKB32n8j9xbPsMZQihfmL3WpUIh9u8t5UPxjwBuOSWYmVuhza::2; __adroll_fpc=76b3cd1ee25f0f80997d6c6b0f53fd86-1595736074261; _fbp=fb.1.1595736074767.210364020; _gid=GA1.2.1153286955.1595996477; __asc=4c7656061739a9974840637ce99; _gat_gtag_UA_46005179_1=1; osCsid=93lptbfloa01anulnvbe0a9jj3; TawkConnectionTime=0; __ar_v4=LM3XUYFU3ZECHJECYX2EJI%3A20200725%3A75%7CYCTJCPNBHJAIPIVE526GC4%3A20200725%3A75%7CG3NB2AWGMJALLM3LQB7B6W%3A20200725%3A75',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    }

    login_data = {
        'action': 'process',
        'email_address': 'londonholder@gmail.com',
        'password': 'ToEQN',
        'x': '33',
        'y': '16',
    }

    with requests.Session() as session:  # open session

        # login
        login_url = 'https://www.wonatrading.com/login'  # url for login page
        request = session.get(login_url, headers=headers)  # request login page
        request = session.post(login_url, data=login_data,
                               headers=headers)  # send data to login

        # request webpage of product
        request = session.get(
            product_page_url, headers=product_headers).content

        soup = BeautifulSoup(request, 'lxml')  # soup = parsed html

        product_name = soup.find('h2').text

        categories = soup.find_all(
            'a', style='font-family:eurof;font-size:14px;')

        # combine all 3 categories and seperate with ; and /
        Category = f'{categories[0].text};{categories[1].text}/{categories[2].text}'

        image1 = soup.find('img', id='main_img')['src']

        try: # try looking for second image
            image2 = soup.find('img', id='des_img')['src']


        except TypeError: # if there's no image it will raise a type error and stop the program
            image2 = '' # all we need is an empty string

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
            # time.sleep(60) # sleep function limits the number of requests over time
            page = scrape_data(page) # page = return of scrape_data function
            data.append(page)  # add data from page

    except AttributeError:      

        # create dataframe
        df = pd.DataFrame(columns=columns, data=data)

        return df    

    # create dataframe
    df = pd.DataFrame(columns=columns, data=data)

    return df
