
## Created by Tim

## Load Modules

import requests                   #Imports the requests module
from bs4 import BeautifulSoup     #Imports the beautiful soup library
import pandas as pd

## Create Data Structures

link_queue = []  # create an empty list to hold the unvisited links
visited_pages = []  # create an empty list to hold the visited links
book_data = {}  # create a dictionary to hold all the information we can scrape from a page

## First, create a list of all unvisited links for book pages

page_num = 0
status_code = 0

while(status_code != 404):  ## Do this until an error is returned (Status_Code 404 is an error)
    page_num = page_num + 1
    index_url = (f"http://books.toscrape.com/catalogue/page-{page_num}.html" )
    page = requests.get(index_url)
    print(f"page number {page_num} has status code {page.status_code}")
    status_code = page.status_code

    if (status_code == 200):  # 200 means a valid page was returned
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="default")
        books = results.find_all("article", class_="product_pod")

        for books in books:

            find_link = books.find("div")
            book_link = f"http://books.toscrape.com/catalogue/{find_link.find('a')['href']}"
            if not(book_link in link_queue):
                link_queue.append(book_link)

## Second, go through each link in the list to populate the book_data dictionary

count = 1
for link in link_queue:

    ##  go through each link
    page = requests.get(link)
    status_code = page.status_code

    if (status_code == 200):  # 200 means a valid page was returned
        soup = BeautifulSoup(page.content, "html.parser")
        book_info = soup.find("div", class_="col-sm-6 product_main")
        title = book_info.find("h1").text

        ## parse out UPC, Price, Availability
        table = soup.find('table', class_='table table-striped')
        rows = table.find_all('tr')   

        UPC = rows[0].find('td').text
        price = rows[2].find('td').text.replace("£","")
        availability = rows[5].find('td').text.replace("In stock (", "").replace(" available)","")

        print(f"Book title {count}: {UPC} {title}")

        ##  add to a python dictionary with the title as key and the rest of the data as a dictionary of key/value pairs
        book_data[UPC] = {'title' : title, 'price' : price, 'availability' : availability}

    count = count + 1
    

## Finally, write the library out to an external data store (file or db)
df = pd.DataFrame(book_data).T

df.to_csv('book_scrapings.csv')
print("Saved as CSV")