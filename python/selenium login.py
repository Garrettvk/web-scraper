from selenium import webdriver
from getpass import getpass

# this is more secure than hard coding the credentials in the file
# username = input("Enter your username: ")
# password = getpass("Enter your password: ")  # hides password being typed

# turn this off in production, use method up top ^
username = 'tmebatson@gmail.com'
password = 'hRIcV'

# path to chromedriver
driver = webdriver.Chrome(r"C:\Users\admin\Anaconda3\Lib\site-packages\chromedriver\chromedriver.exe") 

driver.get(r"https://www.wonatrading.com/login") # wona login page

username_textbox = driver.find_element_by_name('email_address') #find element for email input
username_textbox.send_keys(username) # send what you put as userinput

password_textbox = driver.find_element_by_name('password') #find element for password input
password_textbox.send_keys(username) # send what you put as password

login_button = driver.find_element_by_id('btnLogin') # element of login button
login_button.submit() # simulates hitting enter key