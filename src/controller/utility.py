from bs4 import BeautifulSoup
import pandas as pd
from requests import get
from src.schema import news_model
from src.schema import stock_model
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize 
import matplotlib.pyplot as plt

stopwords = nltk.corpus.stopwords.words('english')

def get_page(string):
    print('\ngetting your page..')
    response = get(string)
    print('parsing your page...')
    html = BeautifulSoup(response.text, 'html.parser')
    print('obtained\n')
    return html


def add_to_database(model):
    try:
        model.save()
        print('\ncreated one event in database with ID: ' + str(model.id) + '\n')
    except:
        print("Error saving to database, moving on...")

def get_stock_symbol(final_company, df, news):
    symbols = []
    for c in final_company:
        if c in news:
            for symbol in df["SYMBOL"].where(df["NAME OF COMPANY"] == c, False):
                if symbol:
                    symbols.append(symbol)
    return symbols

def clean_article(article):
    article = article.replace('/(\n)/gm', " ")
    article = re.sub('[.,!?:;%&$^*@#)/(-''`"—=+]', ' ', article)
    article = re.sub('[0-9]', ' ', article)
    article = article.replace("`|’|”|“", "'")
    article = article.replace("/(\\x)/g", "")
    new_stop_words = ["said", "also", "per", "cent", "would", "last", "first", "like", '\'', '\"', "\'", "\"", "’", "'s", "“", "”"]
    stopwords.extend(new_stop_words)
    clean = [ word for word in word_tokenize(article) if not word in stopwords ]
    return clean

def get_lower_case(article):
    lower = [ word.casefold() for word in article ] 
    return lower

def get_company(news):
    final_company = []
    symbols = []
    clean = clean_article(news)
    news = news.replace("Ltd", "Limited")
    news = news.replace("limited", "Limited")
    data = pd.read_csv(r'./data.csv')
    df = pd.DataFrame(data, columns=['SYMBOL', 'NAME OF COMPANY'])
    companies = data["NAME OF COMPANY"]
    for company in companies:
        inter = [ value for value in word_tokenize(company) if value in clean ]
        if len(inter) > 1:
            if ' '.join(inter) in news:
                final_company.append(company)
                symbols = get_stock_symbol(final_company, df, news)
    return symbols

def sort_dict(dictionary):
    sorted_dict = dict(sorted(dictionary.items(), key = lambda kv: kv[1]))
    return dict(reversed(list(sorted_dict.items())))

def count(el, dictionary):
    if el in dictionary:
        dictionary[el] += 1
    else:
        dictionary.update({el: 1})
    return dictionary

def get_frequency(client):
    word_freq = {}
    sorted_dict = {}
    db = client['eventsdatabase']
    news = db['news']
    news_arr = list(news.find({}))
    for news in news_arr:
        news["article"] = news["article"].replace('/\r?\n|\r/g', " ")
    for news in news_arr:
        clean = clean_article(news["article"])
        lower = get_lower_case(clean)
        for w in lower:
            if len(w) > 2:
                word_freq = count(w, word_freq)
    sorted_dict = sort_dict(dict(word_freq))
    export_as_csv(sorted_dict)

def export_as_csv(dictionary):
    export_dict = {'word': list(dictionary.keys()), 'frequency': list(dictionary.values())}
    df = pd.DataFrame(export_dict)
    df.to_csv('./wordFrequency.csv')

def get_correlation(client):
    rel_comp = []
    db = client['eventsdatabase']
    stocks = db['stocks']
    news = db['news']
    news_arr = list(news.find({
        "company_symbol": {
            "$ne": []
        }    
    })) 

    for news in news_arr:
        if news["company_symbol"] != []:
            for comp in news["company_symbol"]:
                rel_comp.append(comp)
    
    stocks_arr = list(
        stocks.find({
            "symbol": {
                "$in" : rel_comp
            }  
        })
    )

    data = {
        'difference' : [ stock["difference"] for stock in stocks_arr ],
        'subjectivity' : [ news["subjectivity"] for news in news_arr ]
    }

    df = pd.DataFrame(data, columns=['difference', 'subjectivity'])
    plt.scatter(df['difference'], df['subjectivity'])
    plt.savefig('graph.png', bbox_inches='tight')