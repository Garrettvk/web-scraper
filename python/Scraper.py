import time # timing functions
import pandas as pd # data analaysis 
from bs4 import BeautifulSoup # used for web scraping
from selenium import webdriver # creates automated browser
from more_itertools import divide # used for spliting product likes list into equal parts
from selenium.webdriver.common.keys import Keys # used for pressing enter on login screen

class Scraper:

    soup = BeautifulSoup(driver.page_source, 'html5lib')  # soup = parsed html

    def __init__(self, name, category, image_1, image_2, description, cost):
        self.name = name
        self.category = category
        self.image_1 = image_1
        self.image_2 = image_2
        self.description = description
        self.cost = cost
        self.soup = soup
        
