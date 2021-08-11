#!/usr/bin/env python

""" Python program that takes in a wikipedia article link and returns the title, most
    frequent words, and hyperlinks of each section.
    
    Single asterik(*) denotes section, double asterik(**) denotes subsection.
    
    Issues:
    1. Does not return hyperlinks of a section if the section contains hyperlinks in bullet
    points, numbered list, or table format.
    2. For the above reason, program does not return hyperlinks of 'See Also', 'Notes', 
    'References/Bibliography', and 'External Links' sections.
"""

__author__ = "Chiranjeevi Chimmili"
__email__ = "akashchimmili@gmail.com"


import nltk, string, wikipediaapi, requests, os, sys, bs4, json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from urllib.parse import unquote
from bs4 import BeautifulSoup
nltk.download('stopwords')                          # Only need to download once
nltk.download('punkt')                              # Only need to download once


S = requests.Session()
dummyURL = "https://en.wikipedia.org/w/api.php"
URL = input("Enter wikipedia article url: ")       # Asks user for wikipedia link
URL = unquote(URL)
page = URL.split('https://en.wikipedia.org/wiki/')[1]
wiki_wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI)
link = wiki_wiki.page(page)
response = requests.get(URL)


number = 0
def print_page(sections, level=0):                # Main function, prints all the information
    global number
    for section in sections:
        number += 1

        text_no_sw_list = parsed_text(section)
        common_words = find_common_words(text_no_sw_list)
        souping = result(content_of_section(number))

        print("\n%s%s: \n\nMost Frequent Words:" %("*" * (level + 1), section.title))
        if common_words is not None:
            for word in common_words:
                print(word)
        else:
            print("None")
        print("\nHyperlinks:")
        if common_words and souping:
            for s in souping:
                print(s)
        else:
            print("None")
        print_page(section.sections, level + 1)
        print("\n")


def find_common_words(text_list):                   # Finds most frequent words
        counted_list = Counter(text_list)
        if not counted_list:
                return
        return counted_list.most_common(5)


def parsed_text(text_input):                        # Removes stopwords from parsed text
    text = word_tokenize(text_input.text.lower())
    new_text = [''.join(c for c in s if c not in string.punctuation) for s in text]
    new_text = [s for s in new_text if s]

    text_no_sw_list = [word for word in new_text if not word in stopwords.words()]
    return text_no_sw_list


PARAMS3 = {                                        # Params for get_pageid() function
	"action": "query",
	"format": "json",
	"indexpageids": 1,
	"titles": page
}

R3 = S.get(url=dummyURL, params=PARAMS3)
data3 = R3.json()

def get_pageid(dictionary):                        # Retrieves page ID of wiki article
    for key, value in dictionary.items(): 
        if isinstance(value, dict):
            return get_pageid(value)
            
        newdict = {key : value}
        for eachdict in newdict:
            if key == 'pageid':
                return value    


def number_of_sections(dictionary):               # Finds number of sections of wiki article
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


PARAMS1 = {                                      # Params for result() function
    "action": "parse",
    "pageid": get_pageid(data3),
    "prop" : "sections",
    "format": "json"
}

R = S.get(url=dummyURL, params=PARAMS1)
DATA1 = R.json()
x = number_of_sections(DATA1)

def result(soupy):                               # Finds all hyperlinks
    all_links = []
    paragraphs = soupy.find_all('p')
    for p in paragraphs:
        hrefs = p.select('[href]')
        for href in hrefs:
            link = href.get("href")
            if not link.startswith('#'):
                all_links.append(link)
    return all_links    


def links(dictionary):                          # Removes unnecessary hyperlinks
    for key, value in dictionary.items(): 
        if isinstance(value, dict):
            return links(value)
            
        newdict = {key : value}
        for eachdict in newdict:
            if key == '*':
                return value
               

def content_of_section(i):                      # Gets text of a certain section
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


print_page(link.sections)                       # Call to main function
