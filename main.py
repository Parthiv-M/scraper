from mongoengine import connect
print("mongoengine imported")
from src import economic_times
print("economic_times imported")
from src import money_control
print("money_control imported")
from dotenv import load_dotenv
print("dotenv imported")
import os
print("os imported")
from src.controller import utility

load_dotenv()

url_one = os.getenv("URL_ONE")
url_two = os.getenv("URL_TWO")

connect("eventsdatbase", host="localhost", port=27017)

# economic times website

econ = utility.get_page(url_one + "/news")
economic_times.scrape_economic_times(econ)

# money control website

mon = utility.get_page(url_two + "/news")
money_control.scrape_money_control(mon)


# use mongoengine - done
# create object document mapper class - done
# speciy the article as unique - done
# scrape the companies data
# perform correlation
