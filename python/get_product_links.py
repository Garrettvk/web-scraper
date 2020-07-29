from bs4 import BeautifulSoup
import requests
import pandas as pd

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

# product_links = get_product_links()

# print(product_links[1])