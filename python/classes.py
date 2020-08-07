import pandas as pd
import regex as re
from datetime import datetime

'''
    A class is a blueprint for creating instances
    each product that is created is an instance of Product class

    Instance variables contain data that is unique to each instance

    Inheritance lets you use attributes and methods from a parent class
    https://youtu.be/RSl87lqOXDE

    you can use str() and repr() with classes
    its the same as: Class.__str__(), Class.__repr__()

'''


class Product:

    '''
        Class variables contain data that is shared with all instances
        you can only access class variables through the class or an instance of the class

        Change the class and the instances:
            Product.markup = 10

        Change the value for 1 instance:
            Product_1.markup = 4

            Product_1.__dict__ 
                shows that markup is now an instance variable
                this will overide the class variable as long as self.markup is used in price function
                if Product.markup was used, the class variable would be used.
    '''

    count = 0  # incremented as products are created
    markup = 2  # differene between cost price and price
    domain = 'https://www.wonatrading.com/'

    def __init__(self, name, category, image_1, image_2, description, cost):
        # __init__ initializes instances
        # aka constructor

        self.name = name
        self.category = category
        self.image_1 = Product.domain + image_1
        self.image_2 = Product.domain + image_2
        self.description = description
        self.cost = cost
        self.price = self.cost * Product.markup
        self.style = self.get_style_number()
        self.url = self.get_url()
        self.description = self.get_description() # clean description


        # using class name instead of self insures each instance has the same value
        Product.count += 1  # add a product to counter

    def __repr__(self):
        # representation of object for developers
        # use somthing that you can copy and paste back into python code that would recreate the object
        return f'Product({self.name}, {self.category}, {self.image_1}, {self.image_2}, {self.description}, {self.cost},)'

    def __str__(self):
        # representation of object for end users
        # function gets called when print is used
        return self.name

    def __add__(self, other):
        # adds to product prices together
        # you can run this by: self + other
        return self.price() + other.price()

    '''
        These are regular methods, these methods always contain self
        when calling methods you need to use () because you're calling a method not an attribute
    '''

    def get_style_number(self):  # returns product's style number
        pattern = re.compile(r'\d{6}')  # 6 digit pattern
        # look for matches in product description
        matches = pattern.finditer(self.description)
        matches_list = [match.group()
                        for match in matches]  # create a list of each match
        return matches_list[0]  # return first match

    def get_url(self):
        name = self.name.replace(' ', '-')
        return f'{Product.domain}product_info.php?products_id={self.style}&kind=2&cPath=172_93_96&description={name}'

    def get_description(self):
        try: # start description from theme
            start = self.description.index('Theme')
        except ValueError: # use size if there is no theme
            start = self.description.index('Size')
        end = self.description.index(self.name) # end string at product name
        return self.description[start:end].strip() # return string without leading and trailing whitespace

    '''
        Class methods
            class methods are created with decorator and always contain, cls as an argument
            the decorator alters the functionality of the method
            the function receives the class as the first argument 
            rather than the instance

            you can use class methods as alternate constructors
            this allows you to create an object in multiple ways
            alternate constructors start with 'from'
    '''

    @classmethod  # changes markup amount
    def set_markup_amount(cls, amount):
        cls.markup = amount

    @classmethod  # creates product from dataframe data
    def from_dataframe(cls, columns, index):
        name, category, image_1, image_2, description, cost = [
            df.at[index, column] for column in columns]
        return cls(name, category, image_1, image_2, description, cost)

    '''
        Static methods don't pass anything automatically
        they act like regular functions
        we include them in the class because they have a connection to the object

        use static methods when you don't access a class or an instance in the function
    '''

    @staticmethod
    def now():  # this could be used to track when products are created
        return datetime.now()


df = pd.read_csv('csv/24541 products.csv').fillna('')  # open csv as dataframe

# create products from dataframe
Product_1 = Product.from_dataframe(df.columns, 0)
Product_2 = Product.from_dataframe(df.columns, 1)
Product_3 = Product.from_dataframe(df.columns, 2)
Product_4 = Product.from_dataframe(df.columns, 3)


def cls():  # function for clearing shell
    for i in range(40):
        print('')

# exec(open('./python/classes.py').read()) # open python file in shell

# create products with for loop
# products_in_df = df.index.size
# products = [None] * products_in_df # list of each product
# for i in range(products_in_df):
#     products[i] = Product.from_dataframe(df.columns, 0)