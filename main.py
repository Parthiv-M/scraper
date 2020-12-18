from bs4 import BeautifulSoup
print("BeautifulSoup imported")
from requests import get
print("requests imported")
import pymongo
print("PyMongo imported")
from src import economic_times
print("economic_times imported")
from src import money_control
print("money_control imported")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient.eventsdatabase

serverStatusResult = db.command("serverStatus")

# economic times website

economic_times_url = 'https://economictimes.indiatimes.com'

print('\ngetting your page..')
econ_response = get(economic_times_url+'/news')
print('parsing your page...')
economic_page_html = BeautifulSoup(econ_response.text, 'html.parser')
print('obtained economic times\n')

economic_times.scrape_economic_times(economic_page_html, db)

# money control website

money_control_url = 'https://www.moneycontrol.com/'

print('\ngetting your page..')
money_response = get(money_control_url+'/news')
print('parsing your page...')
money_page_html = BeautifulSoup(money_response.text, 'html.parser')
print('obtained money control\n')

money_control.scrape_money_control(money_page_html, db)