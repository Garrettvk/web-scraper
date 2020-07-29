import requests
from bs4 import BeautifulSoup
from get_product_links import get_product_links
from clean_description import *

headers = {
    'cookie': 'cookie_test=please_accept_for_session; __auc=8afe36de17389481e509d9e1c71; _ga=GA1.2.1781461277.1595736073; __tawkuuid=e::wonatrading.com::fl9A0cET/otx3JZxKB32n8j9xbPsMZQihfmL3WpUIh9u8t5UPxjwBuOSWYmVuhza::2; __adroll_fpc=76b3cd1ee25f0f80997d6c6b0f53fd86-1595736074261; _fbp=fb.1.1595736074767.210364020; osCsid=lcau16rhuad4cgo3nqt1g6k103; __asc=e88cdaa517398cd92b44cd05553; _gid=GA1.2.1153286955.1595996477; _gat_gtag_UA_46005179_1=1; TawkConnectionTime=0; __ar_v4=G3NB2AWGMJALLM3LQB7B6W%3A20200725%3A52%7CYCTJCPNBHJAIPIVE526GC4%3A20200725%3A52%7CLM3XUYFU3ZECHJECYX2EJI%3A20200725%3A52',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

product_headers = {
    'cookie' : 'cookie_test=please_accept_for_session; __auc=8afe36de17389481e509d9e1c71; _ga=GA1.2.1781461277.1595736073; __tawkuuid=e::wonatrading.com::fl9A0cET/otx3JZxKB32n8j9xbPsMZQihfmL3WpUIh9u8t5UPxjwBuOSWYmVuhza::2; __adroll_fpc=76b3cd1ee25f0f80997d6c6b0f53fd86-1595736074261; _fbp=fb.1.1595736074767.210364020; _gid=GA1.2.1153286955.1595996477; __asc=4c7656061739a9974840637ce99; _gat_gtag_UA_46005179_1=1; osCsid=93lptbfloa01anulnvbe0a9jj3; TawkConnectionTime=0; __ar_v4=LM3XUYFU3ZECHJECYX2EJI%3A20200725%3A75%7CYCTJCPNBHJAIPIVE526GC4%3A20200725%3A75%7CG3NB2AWGMJALLM3LQB7B6W%3A20200725%3A75',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',    
}

login_data = {
    'action': 'process',
    'email_address': 'londonholder@gmail.com',
    'password': 'ToEQN',
    'x': '33',
    'y': '16',
}

with requests.Session() as session:

    # login
    login_url = 'https://www.wonatrading.com/login' # url for login page
    request = session.get(login_url, headers=headers) # request login page
    request = session.post(login_url, data=login_data, headers=headers)  # send data to login

    product_page_url = get_product_links()[0]  # get product page url
    
    # request webpage of product
    request = session.get(product_page_url, headers=product_headers).content

    soup = BeautifulSoup(request, 'lxml')  # soup = parsed html

    price = soup.find('td', class_='products_info_price').text  # raw price
    price = clean_price(price) # cleaned price

    print(price)

#print(repr(product_link)) # this prints hidden characters!!!
