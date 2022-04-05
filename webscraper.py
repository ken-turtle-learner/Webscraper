# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 08:53:54 2022

@author: RYZEN
"""
import requests                   #Imports the requests module
from bs4 import BeautifulSoup     #Imports the beautiful soup library

# assigns the link of the webpage to a variable
url = "http://books.toscrape.com/"  

page = requests.get(url)


soup = BeautifulSoup(page.content, "html.parser")

"""
Note: You’ll want to pass page.content instead of page.text to avoid problems 
with character encoding. The .content attribute holds raw bytes, which can be 
decoded better than the text representation you printed earlier using 
the .text attribute.

The second argument, "html.parser", makes sure that you use the 
appropriate parser for HTML content.
"""
# "results" finds the specific html element by its ID. 
# The default ID here contains all the elements with the info we need
results = soup.find(id="default")

# I further narrowed down the search to the container that contains the info.
books = results.find_all("article", class_="product_pod")

"""
The loop below searches inside the "product_pod" and executes
the commands in the loop.
"""
for books in books:
    """
    Looks for the H3 tag inside the "product_pod" container
     
    It took a while for me to solve this one here
    The title of the books are inside an <a> tag
    What I did is to search inside the <a> tag and treated the title
    attribute as a dictionary. 
    """
    books_title = books.find("h3")
    book_title = books_title.find('a')["title"]
    print("Title: ",book_title)
    
    """
    The price was pretty straightforward, same as before, I narrowed down the
    search from product_pod to the div with class "product_price", then I
    narrowed it down to the container with the <p> tag which houses the price
    info. I wanted to show only the price, but there are other info inside the
    <p> tag. So I added the .text when I wrote the print statement to only show
    the text.
    """
    books_price = books.find("div", class_="product_price")
    book_price = books_price.find("p")
    print("Price: ",book_price.text)
    
    """
    The instock info in the website shows In stock when a book is available
    so I decided to use boolean to check if the value inside the <p> tag is 
    "In stock"
    """
    in_stock = books_price.find("p", class_="instock availability")
    availability = in_stock.text.strip() == "In stock"
    if availability == True:
        print("In stock: Yes")
    else:
        print("In stock: No")
        
    """
    In the book rating, the data I wanted is the value of the "class" inside
    the <p> tag so unlike what I did above where I was able to define the
    class to find the data, here I needed to make sure that I didn't specify 
    the "class" value so that it works for all the other books.
    
    So I did what I did above where I treated it as a dictionary (but I think
    what it did here is it treated it as a list instead) I'm not really sure
    why it treated it differently though. 
    
    When I printed out the value of book_rating, it showed the correct data
    but its printing it as a list, which doesn't look good, so I added a variable 
    named rate and used a .join on the value of book_rating.
    
    Not sure if this is the most efficient way for this program to be wrtten.
    I'm sure its not LOL. but somehow it worked :D 
    """
    book_rating = books.find("p")["class"]
    rate = " ".join(book_rating)
    print("Rating:", rate.capitalize())
    
    
    print()
    
"""
Original Code inspiration:
import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
job_elements = results.find_all("div", class_="card-content")

for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()
"""