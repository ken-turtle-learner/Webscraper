
## Created by Tim

## Load Modules

import requests                   #Imports the requests module
from bs4 import BeautifulSoup     #Imports the beautiful soup library

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

    if (status_code == 200):
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="default")
        books = results.find_all("article", class_="product_pod")

        for books in books:

            find_link = books.find("div")
            book_link = f"http://books.toscrape.com/{find_link.find('a')['href']}"
            if not(book_link in link_queue):
                link_queue.append(book_link)

## Second, go through each link in the list to populate the book_data dictionary

for link in link_queue:
    print(link)  # just print for now
        
    ##  go through each link 
    ##  parse the information using Beautiful Soup
    ##  add to a python dictionary with the title as key and the rest of the data as a dictionary of key/value pairs

## Finally, write the library out to an external data store (file or db)

