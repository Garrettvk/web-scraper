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

def get_product_links_redo(driver): # this gets every product page

    def get_pages_data(driver):

        def get_pages(driver):

            pages = {}  # dictionary containing page numbers for each category
            
            def get_categories(driver):
                url = r'https://www.wonatrading.com/jewelry' # page that shows categories of jewelry
                class_ = 'category brrem'  # class of html that contains each category
                
                def scrape_hrefs(url, class_, driver):
                    driver.get(url) # open given url
                    soup = BeautifulSoup(driver.page_source, 'html5lib')  # soup = parsed html
                    html_elements = soup.find_all('a', class_ = class_) # html element holding page numbers
                    hrefs_list = [page['href'] for page in html_elements]  # list of links for each category    
                    return hrefs_list # return list of hrefs

                category_hrefs = scrape_hrefs(url, class_, driver)  # list of all the hrefs for wach category
                return category_hrefs

            for category in get_categories(driver):

                driver.get(category)

                # text of element containing # of products converted to an int
                number_of_products = int(driver.find_element_by_xpath('/html/body/div[1]/div/table[2]/tbody/tr/td[3]/table/tbody/tr/td[1]/table/tbody/tr[4]/td/form/table[2]/tbody/tr[4]/td/center/b[3]').text)
                
                def get_number_of_products(number_of_products):

                    products_per_page = 100 # the number of products displayed on each page

                    # divmod returns the # of whole pages and the remainder
                    number_of_pages, remainder = divmod(number_of_products, products_per_page)  

                    if number_of_pages == 0: # if there are 0 pages
                        number_of_pages = 1 # 1 is the lowest amount of pages possible
                    else: # if page > 0
                        if remainder > 0: # if remainder exsists
                            number_of_pages += 1 # add a page

                    return number_of_pages

                number_of_products = get_number_of_products(number_of_products)
                
                pages[f'{category}'] = number_of_products

            return pages
    
        pages = get_pages(driver) # function returns dictionary {'category' : # of products,}

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

    df = get_pages_data(driver) # this returns a dataframe with columns: url, # of Pages, Product Category

    urls_list = []

    for category_index in df.index.tolist():    

        url = df.at[category_index, 'url']

        number_of_pages = df.at[category_index, '# of Pages']

        def get_page_urls(url, number_of_pages): # this function gets urls for every page # 
            page_urls = [] # list containg urls for each page number
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

# exec(open('./python/sample.py').read()) # open python file in shell
