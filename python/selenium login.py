from selenium import webdriver
from getpass import getpass

username_textbox = input("Enter your username: ")
password = getpass("Enter your password: ") # hides password being typed

# path to chromedriver
driver = webdriver.chrome(r"C:\Users\admin\Anaconda3\Lib\site-packages\chromedriver\chromedriver.exe") 

driver.get(r"https://www.wonatrading.com/login") # wona login page

username_textbox = driver.find_element_by_id()