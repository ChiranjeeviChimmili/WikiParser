import nltk, string, wikipediaapi, requests, bs4, json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from urllib.parse import unquote
from bs4 import BeautifulSoup
#nltk.download('stopwords')
#nltk.download('punkt')
S = requests.Session()



dummyURL = "https://en.wikipedia.org/w/api.php"

URL = input("Enter wikipedia article url: ")
URL = unquote(URL)
page = URL.split('https://en.wikipedia.org/wiki/')[1]
wiki_wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI)
link = wiki_wiki.page(page)
response = requests.get(URL)



PARAMS3 = {
	"action": "query",
	"format": "json",
	"indexpageids": 1,
	"titles": page
}

R3 = S.get(url=dummyURL, params=PARAMS3)
data3 = R3.json()

def get_pageid(dictionary):
    for key, value in dictionary.items(): 
        if isinstance(value, dict):
            return get_pageid(value)
            
        newdict = {key : value}
        for eachdict in newdict:
            if key == 'pageid':
                return value    



def result(soupy): 
    allinks = []
    paragraphs = soupy.find_all('p')
    for p in paragraphs:
        m = p.select('[href]')
        for v in m:
            b = v.get("href")
            if not b.startswith('#'):
                allinks.append(b)
    return allinks    


def links(dictionary):
    for key, value in dictionary.items(): 
        if isinstance(value, dict):
            return links(value)
            
        newdict = {key : value}
        for eachdict in newdict:
            if key == '*':
                return value
               

def content_of_section(i):
        PARAMS2 = {
        "action": "parse",
        "pageid": get_pageid(data3),
        "section": i,
        "prop" : "text",
        "format": "json"}  
        P = S.get(url=dummyURL, params=PARAMS2)
        DATA2 = P.json()
        y = links(DATA2)
        soup = BeautifulSoup(y, 'lxml')
        return soup