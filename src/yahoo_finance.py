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

# functino to scrape yahoo website for stock data
def scrape_yahoo():
    tds = []

    data = pd.read_csv(r'./nifty50.csv')

    for symbol in data["Symbol"]:
        sleep(randint(2, 5))
        
        searchString = "https://in.finance.yahoo.com/quote/" + symbol + ".NS/history?p=" + symbol + ".NS&.tsrc=fin-srch"
        yah = utility.get_page(searchString)
        
        if yah.find("tbody").find_all("tr") != None:
            trs = yah.find("tbody").find_all("tr")

        for td in trs[0]:
            tds.append(td)

        if tds[0].span.text is not None:
            model = stock_model.stocks(
                date=tds[0].span.text,
                symbol=symbol,
                opening=locale.atof(tds[1].span.text),
                closing=locale.atof(tds[4].span.text),
                difference=((locale.atof(tds[4].span.text)) - (locale.atof(tds[1].span.text))) 
            )

        tds.clear()

        utility.add_to_database(model)
