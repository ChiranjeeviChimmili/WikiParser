
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

number = 0
def print_page(sections, level=0):
    global number
    for section in sections:
        number += 1

        text_no_sw_list = parsed_text(section)
        common_words = find_common_words(text_no_sw_list)
        souping = content_of_section(number)

        print("\n%s%s: \nMost Frequent Words: %s\n\n" % ("*" * (level + 1), section.title, common_words))
        if common_words and result(souping):
            print("Hyperlinks:", result(souping))
        print_page(section.sections, level + 1)
        print("\n")



def find_common_words(text_list):        
        counted_list = Counter(text_list)
        if not counted_list:
                return ""
        return counted_list.most_common(5)


def parsed_text(text_input):
    text = word_tokenize(text_input.text.lower())
    new_text = [''.join(c for c in s if c not in string.punctuation) for s in text]
    new_text = [s for s in new_text if s]

    text_no_sw_list = [word for word in new_text if not word in stopwords.words()]
    return text_no_sw_list

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


def number_of_sections(dictionary):
    last_section = 0
    for key, value in dictionary.items(): 
        if isinstance(value, dict):
            return number_of_sections(value)
            
        newdict = {key : value}
        for eachdict in newdict:
            if key == 'sections':
                sections_dict = value
                for eachdict in sections_dict:
                    for key, value in eachdict.items():
                        if key == 'index':
                                last_section += 1   
                return last_section  


PARAMS1 = {
    "action": "parse",
    "pageid": get_pageid(data3),
    "prop" : "sections",
    "format": "json"
}

R = S.get(url=dummyURL, params=PARAMS1)
DATA1 = R.json()
x = number_of_sections(DATA1)
 


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


print_page(link.sections)



