import requests
from bs4 import BeautifulSoup

headers = {
    'cookie': 'cookie_test=please_accept_for_session; __auc=8afe36de17389481e509d9e1c71; _ga=GA1.2.1781461277.1595736073; __tawkuuid=e::wonatrading.com::fl9A0cET/otx3JZxKB32n8j9xbPsMZQihfmL3WpUIh9u8t5UPxjwBuOSWYmVuhza::2; __adroll_fpc=76b3cd1ee25f0f80997d6c6b0f53fd86-1595736074261; _fbp=fb.1.1595736074767.210364020; osCsid=lcau16rhuad4cgo3nqt1g6k103; __asc=e88cdaa517398cd92b44cd05553; _gid=GA1.2.1153286955.1595996477; _gat_gtag_UA_46005179_1=1; TawkConnectionTime=0; __ar_v4=G3NB2AWGMJALLM3LQB7B6W%3A20200725%3A52%7CYCTJCPNBHJAIPIVE526GC4%3A20200725%3A52%7CLM3XUYFU3ZECHJECYX2EJI%3A20200725%3A52',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    
}

product_headers = {
    'cookie': 'cookie_test=please_accept_for_session; __auc=8afe36de17389481e509d9e1c71; _ga=GA1.2.1781461277.1595736073; __tawkuuid=e::wonatrading.com::fl9A0cET/otx3JZxKB32n8j9xbPsMZQihfmL3WpUIh9u8t5UPxjwBuOSWYmVuhza::2; __adroll_fpc=76b3cd1ee25f0f80997d6c6b0f53fd86-1595736074261; _fbp=fb.1.1595736074767.210364020; __asc=e88cdaa517398cd92b44cd05553; _gid=GA1.2.1153286955.1595996477; osCsid=o9t4vidjg18hblbpoj8h93chc1; _gat_gtag_UA_46005179_1=1; TawkConnectionTime=0; __ar_v4=G3NB2AWGMJALLM3LQB7B6W%3A20200725%3A58%7CYCTJCPNBHJAIPIVE526GC4%3A20200725%3A58%7CLM3XUYFU3ZECHJECYX2EJI%3A20200725%3A58',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',    
}

login_data = {
    'action': 'process',
    'email_address': 'londonholder@gmail.com',
    'password': 'ToEQN',
    'x': '33',
    'y': '16',
}

product_links = [] # this is product urls for all the products on the first page

with requests.Session() as session:

    # login
    login_url = 'https://www.wonatrading.com/login' # url for login page
    request = session.get(login_url, headers=headers) # request login page
    request = session.post(login_url, data=login_data, headers=headers)  # send data to login
    
    # get product page
    product_url = 'https://www.wonatrading.com/jewelry/anklet'  # url for products page    
    # the response of this get request is the webpage of all the jewelry anklet products
    product_page = session.get(product_url, headers=product_headers)

    soup = BeautifulSoup(product_page.content, 'lxml')  # soup = parsed html

    # this html element contains the href for the product
    products = soup.find_all('a', style="position:relative;float:left;")

    # since the href doesn't have the domain included, we need to add it 
    domain = 'https://www.wonatrading.com/'

    for product in products: # iterate of each product on webpage
        product_link = product['href']  # product_link = this href
        product_link = product_link.replace('\r\n', '')  # remove hidden characters from product link
        product_links.append(f'{domain}{product_link}') # combine the domain and product_link

print('\n'.join(product_links))  # prints page after login

#print(repr(product_link)) # this prints hidden characters!!!
