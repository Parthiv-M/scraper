from bs4 import BeautifulSoup
print("BeautifulSoup imported")
from requests import get
print("requests imported")
from mongoengine import connect
print("mongoengine imported") 
import pymongo
print("PyMongo imported")
from src import economic_times
print("economic_times imported")
from src import money_control
print("money_control imported")
from dotenv import load_dotenv
print("dotenv imported")
import os
print("os imported")

load_dotenv()

url_one = os.getenv("URL_ONE")
url_two = os.getenv("URL_TWO")

connect("eventsdatbase", host="localhost", port=27017)

# economic times website

print('\ngetting your page..')
econ_response = get(url_one+'/news')
print('parsing your page...')
economic_page_html = BeautifulSoup(econ_response.text, 'html.parser')
print('obtained economic times\n')

economic_times.scrape_economic_times(economic_page_html)

# money control website

print('\ngetting your page..')
money_response = get(url_two+'/news')
print('parsing your page...')
money_page_html = BeautifulSoup(money_response.text, 'html.parser')
print('obtained money control\n')

money_control.scrape_money_control(money_page_html)


# use mongoengine - done
# create object document mapper class - done
# speciy the article as unique - done
# scrape the companies data
# perform correlation
