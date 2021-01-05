import pandas as pd
from time import sleep
from random import randint
from dotenv import load_dotenv
import os
import locale
from src.schema import stock_model
from src.controller import utility

load_dotenv()
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def scrape_yahoo():
    symbol = []
    tds = []

    data = pd.read_csv(r'./nifty50.csv')

    for symbol in data["Symbol"]:
        sleep(randint(2, 5))
        searchString = "https://in.finance.yahoo.com/quote/" + symbol + ".NS/history?p=" + symbol + ".NS&.tsrc=fin-srch"
        yah = utility.get_page(searchString)
        trs = yah.find("tbody").find_all("tr")

        for td in trs[0]:
            tds.append(td)
        
        model = stock_model.stocks(
            date=tds[0].string,
            symbol=symbol,
            opening=locale.atof(tds[1].string),
            closing=locale.atof(tds[4].string),
            difference=((locale.atof(tds[4].string)) - (locale.atof(tds[1].string))) 
        )

        print(model.opening)
        print(model.difference)

        tds.clear()

        utility.add_to_database(model)
