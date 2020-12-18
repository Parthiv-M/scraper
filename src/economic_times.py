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

base_page_link = 'https://economictimes.indiatimes.com' 

def add_to_database(db, data):
    result = db.events.insert_one(data.copy())
    print('\ncreated one event in database with ID: ' + str(result.inserted_id) + '\n')

def sub_page(link, db):
    print('\nin sub-page function')
    subpage_response = get(link)
    subpage = BeautifulSoup(subpage_response.text, 'html.parser')
    
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
    
    data_object['date'] = ''.join(date_time.split(' ')[2:5])
    data_object['time'] = ''.join(date_time.split(' ')[5:])
    data_object['article'] = article.text
    data_object['subjectivity'] = TextBlob(article.text).sentiment.subjectivity
    data_object['polarity'] = TextBlob(article.text).sentiment.polarity

    add_to_database(db, data_object)

def sub_news(name, link, db):
    print('\nin ' + str(name))
    sub_resposne = get(link)
    sub = BeautifulSoup(sub_resposne.text, 'html.parser')
    tabs = []
    links = []
    tabs = sub.find_all('div', class_='eachStory')
    for i in tqdm(range(0, len(tabs))):
        links.append(tabs[i].h3.a.get('href'))
    for i in tqdm(range(0, len(links))):
        sub_page(base_page_link + links[i], db)

def economy_page(link, db):
    h_left = []
    h_right = []
    econ_response = get(link)
    econ = BeautifulSoup(econ_response.text, 'html.parser')
    sub_left = econ.find_all('div', class_='flt secBox')
    sub_right = econ.find_all('div', class_='flr secBox')
    for i in range(0, len(sub_left)):
        h_left.append(sub_left[i].h2.a.get('href'))
    for i in range(0, len(sub_right)):
        h_right.append(sub_right[i].h2.a.get('href'))
    for i in tqdm(range(0, len(h_right))):
        sub_news(sub_right[i].h2.text, h_right[i], db)
    for i in tqdm(range(0, len(h_left))):
        sub_news(sub_left[i].h2.text, h_left[i], db)

def scrape_economic_times(page_html, db):
    h_left = []
    h_right = []
    
    subsec_left = page_html.find_all('section', class_='subsecNews flt')
    subsec_right = page_html.find_all('section', class_='subsecNews flr')

    for i in tqdm(range(0, len(subsec_left))):
        h_left.append(subsec_left[i].h2.a.get('href')) 
    for i in tqdm(range(0, len(subsec_right))):
        h_right.append(subsec_right[i].h2.a.get('href')) 
        
    economy_page(h_left[0] ,db)
    for news in range(1, len(h_left)):
        sub_news(subsec_left[i], h_left[i], db)
    for news in range(0, len(h_right)):
        sub_news(subsec_right[i], h_right[i], db)
    