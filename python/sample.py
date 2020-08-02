import csv
output = {'anklet': 2, 'bracelet': 85, 'brooch': 7, 'body-jewelry': 2, 'cubic-zirconia': 15, 'earring': 137, 'mask': 4, 'necklace': 73,
          'pendant-set': 3, 'rlace': 73, 'pendant-set': 3, 'ring': 9, 'stainless-steel': 1, 'watch': 1, 'jewelry-component': 1, 'jewelry-display': 1}


dict = output
w = csv.writer(open("output.csv", "w"))
for key, val in dict.items():
    w.writerow([key, val])