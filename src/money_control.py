from tqdm import tqdm
from time import sleep
from random import randint
from textblob import TextBlob
import os
from src.schema import news_model
from src.controller import utility

# function to scrape the money control website
def scrape_money_control(page_html):
    boxes = []
    page_links = []
    boxes = page_html.find_all('section', class_='block2')
    page_links = [ box.h2.a.get('href') for box in boxes ]
    for i in tqdm(range(2, len(page_links) - 1)):
        scrape_next_page(page_links[i])

# function to scrape the next page of money control
def scrape_next_page(link):
    link_html = utility.get_page(link)
    tabs = []
    tab_links = []
    tabs = link_html.find('div', class_='fleft').find_all('li', class_='clearfix')
    tab_links = [ tab.a.get('href') for tab in tabs ]
    for i in tqdm(range(0, len(tab_links))):
        scrape_news(tab_links[i])
        sleep(randint(5, 15))

#  function to scrape each news
def scrape_news(link):
    news_html = utility.get_page(link)
    article = []
    p_text = []
    if(news_html.find('div', class_='content_wrapper arti-flow') != None):
        article = news_html.find('div', class_='content_wrapper arti-flow').find_all('p')
    p_text = [ article.text for article in article ]
    article_text = " ".join(p_text)
    if article_text == "" or article_text == " ":
        return
    if(news_html.find('div', class_='article_schedule') != None):
        date_time = news_html.find('div', class_='article_schedule').text
    else:
        return
    
    date = date_time.split("/")[0]
    time = date_time.split("/")[1]

    symbols = utility.get_company(article_text)

    model = news_model.news(
        date=date,
        time=time,
        article=article_text,
        subjectivity=TextBlob(article_text).sentiment.subjectivity,
        polarity=TextBlob(article_text).sentiment.polarity,
        company_symbol=symbols
    )
    
    utility.add_to_database(model)
    
    sleep(randint(2, 8))