from bs4 import BeautifulSoup
from requests import get
import sys

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