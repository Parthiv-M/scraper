from bs4 import BeautifulSoup
print("BeautifulSoup imported")
from requests import get
print("requests imported")
from pprint import pprint
print("pprint imported")
from tqdm import tqdm
print("tqdm imported")
from time import sleep
print("sleep imported")
from random import randint
print("randomint imported")
from textblob import TextBlob
print("textblob imported")

data_object = {
    'date': '', 
    'time' : '',
    'article': '',
    'subjectivity': '',
    'polarity' : ''
}

base_page_link = 'https://www.moneycontrol.com/'

def add_to_database(db, data):
    result = db.events.insert_one(data.copy())
    print('\ncreated one event in database with ID: ' + str(result.inserted_id) + '\n')

def scrape_money_control(page_html, db):
    boxes = []
    page_links = []
    boxes = page_html.find_all('section', class_='block2')
    for i in tqdm(range(2, len(boxes)-1)):
        page_links.append(boxes[i].h2.a.get('href'))
        sleep(randint(5, 15))
    for i in tqdm(range(0, len(page_links))):
        scrape_next_page(page_links[i], db)
        sleep(randint(5, 15))

def scrape_next_page(link, db):
    print('getting next page..')
    resp = get(link)
    print('parsing next page...')
    link_html = BeautifulSoup(resp.text, 'html.parser')
    print('obtained next page')
    tabs = [];
    tab_links = []
    tabs = link_html.find('div', class_='fleft').find_all('li', class_='clearfix')
    for i in tqdm(range(0, len(tabs))):
        tab_links.append(tabs[i].a.get('href'))
#         pprint(tab_links[i])
        sleep(randint(5, 15))
    for i in tqdm(range(0, len(tab_links))):
        scrape_news(tab_links[i], db)
        sleep(randint(5, 15))

def scrape_news(link, db):
    print('getting news page..')
    news = get(link)
    print('parsing news page...')
    news_html = BeautifulSoup(news.text, 'html.parser')
    print('obtained news page')
    article = []
    p_text = []
    if(news_html.find('div', class_='content_wrapper arti-flow') != None):
        article = news_html.find('div', class_='content_wrapper arti-flow').find_all('p')
    for i  in tqdm(range(0, len(article))):
        p_text.append(article[i].text)
    article_text = " ".join(p_text)
    if article_text == "" or article_text == " ":
        return
    if(news_html.find('div', class_='article_schedule') != None):
        date_time = news_html.find('div', class_='article_schedule').text
    else:
        return
    
    date = date_time.split("/")[0]
    time = date_time.split("/")[1]
    
    data_object['date'] = date
    data_object['time'] = time
    data_object['article'] = article_text
    data_object['subjectivity'] = TextBlob(article_text).sentiment.subjectivity
    data_object['polarity'] = TextBlob(article_text).sentiment.polarity
    
    print('date: ' + data_object['date'])
    print('time: ' + data_object['time'])
    print('article: exists')
    print('subjectivity: '+ str(data_object['subjectivity']))
    print('polarity: '+ str(data_object['polarity']))
    
    add_to_database(db, data_object)
    
    sleep(randint(2, 8))