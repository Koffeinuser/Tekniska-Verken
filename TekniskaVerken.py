# App that scrapes a web page and presents the opening hours in Home Assistant

import bs4
import requests

res = requests.get(
    'https://www.tekniskaverken.se/privat/avfall-och-atervinning/atervinningscentralerna/malmen/')

soup = bs4.BeautifulSoup(res.text, 'html5lib')
for i in soup.select('.openinghours-status'):
    print(i.text)
    
    
