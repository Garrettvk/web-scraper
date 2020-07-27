def clean_description(input_string):

    remove_list = ['�', '\n', '\t', '•'] # items to remove

    for element in remove_list: # iterate over items in list
        input_string = input_string.replace(element, '') # remove each item

    return input_string.strip() # return cleaned input string

def clean_price(input_string):
    # $4.25 / pc

    remove_list = ['$', '/ pc', '\n',] # items to remove

    for element in remove_list: # iterate over items in list
        input_string = input_string.replace(element, '') # remove each item

    return input_string.strip()