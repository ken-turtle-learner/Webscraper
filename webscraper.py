# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 08:53:54 2022

@author: RYZEN
"""
import csv
import requests                   #Imports the requests module
from bs4 import BeautifulSoup     #Imports the beautiful soup library

# assigns the link of the webpage to a variable

search = "ongoing"
outfile = open("Library.csv", 'w', newline='')
page_number = 1

"""
This looops the function up until the last page
"""
header = ["Book Title", "Price", "Availability", "Rating"]
csv.writer(outfile).writerow(header)
while page_number < 51:
    main_url = ("http://books.toscrape.com/catalogue/page-"
                + str(page_number) + ".html")
    page = requests.get(main_url)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="default")
    books = results.find_all("article", class_="product_pod")
    for books in books:

        find_title = books.find("h3")
        book_title = find_title.find('a')["title"]
        print("Title: ", book_title)
        find_price = books.find("div", class_="product_price")
        book_price = find_price.find("p")
        print("Price: ", book_price.text)
        in_stock = find_price.find("p", class_="instock availability")
        availability = in_stock.text.strip() == "In stock"
        if availability is True:
            print("In stock: Yes")
        else:
            print("In stock: No")

        find_rating = books.p["class"][1]

        print("Rating:", find_rating.capitalize(), "out of five stars")
        """
        This adds the data into the list data_item
        """

        data_item = []
        data_item.append(book_title)
        data_item.append(book_price.text)
        if availability is True:
            data_item.append("In Stock")
        elif availability is False:
            data_item.append("Out of Stock")
        data_item.append(find_rating + " out of five stars")
        csv.writer(outfile).writerow(data_item)
    """
   # This adds 1 to the page number to indicate which page to go to next
    """
    page_number = page_number + 1

outfile.close()
