from requests import get
from bs4 import BeautifulSoup
import pandas as pd

SOURCE_URL = 'https://www.foyles.co.uk/new-books?cCode=MT'


def open_doc(url_path):
    response = get(url_path)
    contents = response.text
    soup = BeautifulSoup(contents, 'html.parser')
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(response))
    return soup


def get_data(doc, output):
    try:
        for item in doc.find_all('div', attrs={'class':'CellItem'}):
            output.append(item.attrs)
        print('Success! Data was pulled.')
        return output
    except Exception as err:
        print(f'Oh no! {err}')   

def clean_data(output, key):
    for i in output:
        if key in i:
            del i[key]
    return output

def get_urls(doc):
    urls =[]
    source = doc.find_all('div', class_='BookTitle')

    for article in source:
        for link in article.find_all('a', href=True):
            url = link['href']
            links = 'https://www.foyles.co.uk/witem/' + url
            if links not in urls:
                urls.append(links)
    return urls

def get_authors(doc):
    source = doc.find_all('div', attrs={'class':'Author'})
    authors= []
    for item in source:
        authors.append(item.get_text())
    return authors

def compile_data(url_path):
    data = open_doc(SOURCE_URL)
    attribute_list = []
    to_remove = 'class'

    try:
        get_data(data, attribute_list)
        clean_data(attribute_list, to_remove)
        
        df = pd.DataFrame(attribute_list)
        saved = df.to_csv('test.csv', index= None)
        return 'Data fetched and compiled', saved
    except Exception as err:
        print(f'Oh no! {err}')
    


compile_data(SOURCE_URL)

#TODO: Add URLs and Authors to DF with below functions:
# get_urls(data)
# get_authors(data)

# TODO: Convert price from str into currency format

# TODO: Add functionality and easy accessibility via terminal:
# script creates csv file with data based on command



#









