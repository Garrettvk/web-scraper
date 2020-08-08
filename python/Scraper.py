import re
import csv
import pandas as pd  # data analaysis
from bs4 import BeautifulSoup  # used for web scraping
from selenium import webdriver # creates automated browser


def get_driver(login_on = False): # return driver with no images
    options = webdriver.ChromeOptions() # create option
    prefs = {"profile.managed_default_content_settings.images": 2} # preference to disable images
    options.add_experimental_option("prefs", prefs) # add option
    driver = webdriver.Chrome(options=options) # add option o webdriver
    # driver = login(driver) if login_on else driver # login diver
    return driver  # return driver
    
def get_visted():
    current_data = pd.read_csv('csv/webscraper_output.csv').fillna('') # open current data csv
    return current_data['URL'].tolist() # return list of visted urls

driver = get_driver()

class Scraper:

    domain = 'http://www.wonatrading.com/'

    # path to chromedriver
    # driver = webdriver.Chrome(r'C:\Anaconda\Lib\site-packages\chromedriver_win32\chromedriver.exe')

    def __init__(self, url):
        self.url = url

        driver.get(self.url)  # first product page    

        soup = BeautifulSoup(driver.page_source, 'html5lib')  # soup = parsed html    

        # data from html elements
        try:
            self.name = soup.find('h2').text
        except AttributeError:
            return

        self.categories = soup.find_all('a', style='font-family:eurof;font-size:14px;')
        self.categories = self.get_catagories()
        self.image_1 = self.domain + soup.find('img', id='main_img')['src']

        try: # some products don't have a 2nd image
            self.image_2 = self.domain + soup.find('img', id='des_img')['src']
        except TypeError:
            self.image_2 = '' # leave an empty string

        # create and clean description
        self.description = soup.find('td', class_='tdBorder').find('p').text
        description_patterns = [
            '•',
            '\n',
            '\t',
            self.name,
            r'( Style No : )\d+\s',
            r'((Color : )\w+\s|(Color : )\w+,\s*\w+\s*)'
        ]
        self.style = self.get_style() # get style before its removed
        self.description = self.clean_data(description_patterns, self.description)

        # create and clean price
        self.price = soup.find('td', class_='products_info_price').text
        price_patterns = [
            ' / pc',
            '\$'
        ]
        self.price = self.clean_data(price_patterns, self.price)    

    def clean_data(self, patterns = [], target = None):
        for pattern in patterns: # remove patterns and ignorecase
            target = re.sub(pattern, '', target, flags=re.IGNORECASE)
        return target.strip()

    def get_catagories(self): # return all 3 categories formated
        return f'{self.categories[0].text};{self.categories[1].text}/{self.categories[2].text}'

    def get_style(self):
        pattern = re.compile('\d{5}\d*')
        matches = pattern.finditer(self.description)      # iterate over product descriptions
    
        matches_list = [match.group() for match in matches] # create a list of each match

        return matches_list[0].strip() # return 6 digit style number

links = ['https://www.wonatrading.com/product_info.php?products_id=482328&kind=2&cPath=172_93_96&description=White-Gold-Dipped-Metal-Bar-Station-Anklet',
'https://www.wonatrading.com/product_info.php?products_id=482465&kind=2&cPath=172_98&description=Two-Tone-Metal-Starfish-Pendant-Set',
'https://www.wonatrading.com/product_info.php?products_id=479524&kind=2&cPath=172_93_96&description=4PCS---Baby-Rhinestone-Chain-Layered-Anklets',
'https://www.wonatrading.com/product_info.php?products_id=600520&kind=2&cPath=172_93_96&description=4PCS---Baby-Rhinestone-Chain-Layered-Anklets' ]


df_list = []

for link in links:

    if link in get_visted():
        print('skip')
    else:

        scrape_1 = Scraper(link)  # scraper object which takes url to be scraped
        
        columns = ['Product Name', 'Category', 'Product Image File - 1', 'Product Image File - 2', 'Product Description', 'Cost Price', 'URL', 'Style #']
        
        try:
            data = [scrape_1.name, scrape_1.categories, scrape_1.image_1, scrape_1.image_2, scrape_1.description, scrape_1.price, scrape_1.url, scrape_1.style]
        except AttributeError:
            break

        df = pd.DataFrame(columns=columns, data=[data])

        df_list.append(df)


        # print(scrape_1.name)
        # print(scrape_1.categories)
        # print(scrape_1.image_1)
        # print(scrape_1.image_2)
        # print(scrape_1.description)
        # print(scrape_1.price)
        # print(scrape_1.url)
        # print(scrape_1.style)

output_df = pd.concat(df_list)

output_df.to_csv('csv/webscraper_output.csv', mode='a', index=False, header = False) # 

