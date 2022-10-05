from ast import expr_context
from email import header
import requests
from bs4 import BeautifulSoup
import csv
import os 
import json

#{"Payhip_Link", "Product_Title", "Product_Price", "Product_Image"]

#dir_path = os.path.dirname(os.path.realpath(__file__))
#csv_file_path = dir_path + "/webscrape_dump.csv"

#URL Input
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


links = []
images = []
titles = []
prices = []
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
        links[product] = links[product]['href']
        images[product] = images[product]['src']
        titles[product] = titles[product].text
        prices[product] = prices[product].text.split()[0]

#write to json
json_data = [{"Payhip_Link": l, "Product_Title": t, "Product_Price" : p, "Product_Image": i} for l, t, p, i in zip(links, images, titles, prices)]
with open('webscrape_dump.json', 'w+') as f:
    json.dump(json_data, f, indent=2)