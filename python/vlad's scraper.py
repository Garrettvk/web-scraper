import requests
from bs4 import BeautifulSoup as bs

URL = 'https://www.wonatrading.com/'
LOGIN_ROUTE = '/login'
ANOTHER_ROUTE = '/jewelry/anklet'


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'origin': URL, 'referer': URL + LOGIN_ROUTE}
HEADERS_JEWELRY = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'origin': URL, 'referer': URL + ANOTHER_ROUTE}

s = requests.session()
# csrf_token = s.get(URL).cookies['csrftoken']

login_payload = {
    'email_address': 'londonholder@gmail.com',
    'password': 'ToEQN'
}

login_req = s.post(URL + LOGIN_ROUTE, headers=HEADERS, data=login_payload)
print('STATUS CODE: ', login_req.status_code)
cookies = login_req.cookies

this_req = s.post(URL + ANOTHER_ROUTE, headers=HEADERS_JEWELRY)
print('STATUS CODE: ', this_req.status_code)
cookies = this_req.cookies

# url of html file to download
url = 'https://www.wonatrading.com/product_info.php?products_id=482327&kind=2&cPath=172_93_96&description=Gold-Dipped-Metal-Bar-Station-Anklet'

soup = bs(s.get(url, headers=HEADERS).text, 'html.parser')

print(soup.find('td', class_='products_info_price').text)