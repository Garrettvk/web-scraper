import urllib.request

print('Beginning file download with urllib2...')

# url of html file to download
url = 'https://www.wonatrading.com/product_info.php?products_id=482327&kind=2&cPath=172_93_96&description=Gold-Dipped-Metal-Bar-Station-Anklet'

# request for webpage, this does not retrieve price because you're not logged in
urllib.request.urlretrieve(url, 'C:/Users/admin/Desktop/web-scraper/html/simple.html')