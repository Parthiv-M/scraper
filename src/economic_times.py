from tqdm import tqdm
from time import sleep
from random import randint
from textblob import TextBlob
from dotenv import load_dotenv
import os
from src.schema import news_model 
from src.controller import utility

load_dotenv()

url_one = os.getenv("URL_ONE")

def sub_page(link):
    subpage = utility.get_page(link)
    
    if(subpage.find('time') != None):
        date_time = subpage.find('time').text
    
    if(subpage.find('span',class_='cSprite icon_pp')):  # prime article
        print('prime article')
        return
    if(subpage.find('div', class_='clearfix relTopics raltedTopics') != None):
        subpage.find('div', class_='clearfix relTopics raltedTopics').decompose()
    if(subpage.find('div', class_='disclamerText') != None):
        subpage.find('div', class_='disclamerText').decompose()
    if(subpage.find('section', class_='clearfix rel-art also_read alr') != None):
        subpage.find('section', class_='clearfix rel-art also_read alr').decompose()
    if(subpage.find('section', class_='cmnts_wrapper clearfix') != None): 
        subpage.find('section', class_='cmnts_wrapper clearfix').decompose()
    
    if(subpage.find('article') != None):
        article = subpage.find('article')
    else: 
        return
    
    symbols = utility.get_company(article.text)

    model = news_model.news(
        date=''.join(date_time.split(' ')[2:5]),
        time=''.join(date_time.split(' ')[5:]),
        article=article.text,
        subjectivity=TextBlob(article.text).sentiment.subjectivity,
        polarity=TextBlob(article.text).sentiment.polarity,
        company_symbol=symbols
    )
    
    utility.add_to_database(model)

def sub_news(name, link):
    sub = utility.get_page(link)
    tabs = []
    links = []
    tabs = sub.find_all('div', class_='eachStory')
    links = [ tab.h3.a.get('href') for tab in tabs if tab.h3 != None] 
    for i in tqdm(range(0, len(links))):
        sub_page(url_one + links[i])

def economy_page(link):
    h_left = []
    h_right = []
    econ = utility.get_page(link)
    sub_left = econ.find_all('div', class_='flt secBox')
    sub_right = econ.find_all('div', class_='flr secBox')
    h_left = [ left.h2.a.get('href') for left in sub_left ]
    h_right = [ right.h2.a.get('href') for right in sub_right ]
    for i in tqdm(range(0, len(h_right))):
        sub_news(sub_right[i].h2.text, h_right[i])
    for i in tqdm(range(0, len(h_left))):
        sub_news(sub_left[i].h2.text, h_left[i])

def scrape_economic_times(page_html):
    h_left = []
    h_right = []
    subsec_left = page_html.find_all('section', class_='subsecNews flt')
    subsec_right = page_html.find_all('section', class_='subsecNews flr')
    h_left = [ left.h2.a.get('href') for left in subsec_left ]
    h_right = [ right.h2.a.get('href') for right in subsec_right ]
    economy_page(h_left[0])
    for i in range(1, len(h_left)):
        sub_news(subsec_left[i], h_left[i])
    for i in range(0, len(h_right)):
        sub_news(subsec_right[i], h_right[i])
    