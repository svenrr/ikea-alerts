# -*- coding: utf-8 -*-

"""
ToDo: 
    - Autoscraper
    - REST API Call to x? 
    - Push Up via App?
    - Send WhatsApp Message - Twillo?
"""

import requests 
from lxml import html
from bs4 import BeautifulSoup
import bs4
import re

def main(url):
    x = status(url)
    
    if x == "Kann nicht geliefert ":
        print("Nicht lieferbar")
    else:
        print("Jetzt lieferbar!")
    
def status(url):
    #htree = html.fromstring(requests.get(url).content)
    
    r = requests.get(url)#.content
    if r.status_code == 200:
        soup: bs4.BeautifulSoup = BeautifulSoup(r.content, "html.parser")
    
    #for headline in soup.find_all("span", {"class": "mw-headline"}):
        htree = soup.find_all("span", {"class": "range-revamp-indicator__no-wrap"})
        

        #pat = r'.*?\>(.*)<.*'             #See Note at the bottom of the answer
        #s = str(htree)
        #match = re.match(pat, s) #re.search(pat, s)
        #htree = 
        
        pattern = ">(.*?)<"
        s = str(htree)
        substring = re.search(pattern, s)
        #print(substring)
    
    return substring.group(1)

if __name__ == "__main__": 
    url = "https://www.ikea.com/de/de/p/vallfjaellet-drehstuhl-mit-armlehnen-kopfstuetze-gunnared-grau-s89392189/"
    main(url)