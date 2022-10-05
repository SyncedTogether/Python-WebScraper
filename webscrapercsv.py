from ast import expr_context
from email import header
import requests
from bs4 import BeautifulSoup
import csv
import os 

csv_header = ["Payhip_Link", "Product_Title", "Product_Price", "Product_Image"]
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_file_path = dir_path + "/webscrape_dump.csv"

#URL Input
product_array =[]
URL = input("URL: ")

#assign URL
try:
    page = requests.get(URL)
except:
    print("Invalid URL")
    quit()

#define html parser
soup = BeautifulSoup(page.content, "html.parser")
#scope into page-collection
results = soup.find(id="page-collection")
products = results.find_all("div", class_="product-list-block")

#iterate through product-list-block (even though its just one)
for i in range(len(products)):
    #get all attributes
    links = products[i].find_all("a", class_="grid-item-link")
    prices = products[i].find_all("div", class_="price")
    titles = products[i].find_all("span", class_="text")
    images = products[i].find_all("img", class_="section-image-fallback")


    #make sure reading of attributes are correct
    if (len(prices) == len(titles) and len(titles) == len(images)):
        num_product = len(prices)
    else:
        print("Something went wrong")
    
    for product in range(num_product):
        link = links[product]['href']
        img = images[product]['src']
        title = titles[product].text
        price = prices[product].text.split()[0]
        product_info = [link, img, title, price]
        product_array.append(product_info)

#write to csv
with open(csv_file_path, 'w', encoding='UTF8', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # write the header
    csv_writer.writerow(csv_header)

    # write the data
    for product_data in product_array:
        csv_writer.writerow(product_data)
