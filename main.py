from mongoengine import connect
from src import economic_times
from src import money_control
from src import yahoo_finance
from dotenv import load_dotenv
import os
from src.schema import stock_model
from src.controller import utility

load_dotenv()

url_one = os.getenv("URL_ONE")
url_two = os.getenv("URL_TWO")

client = connect("eventsdatabase", host="localhost", port=27017)

# yahoo finance for getting stock values
if stock_model.stocks:
    stock_model.stocks.drop_collection()
yahoo_finance.scrape_yahoo()

# economic times website
econ = utility.get_page(url_one + "/news")
economic_times.scrape_economic_times(econ)

# money control website
mon = utility.get_page(url_two + "/news")
money_control.scrape_money_control(mon)

# getting the frequency of words present across all articles in the database
utility.get_frequency(client)