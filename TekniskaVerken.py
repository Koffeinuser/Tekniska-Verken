# App that scrapes a web page and presents the opening hours in Home Assistant

Home Assistant
import bs4
import requests
res = requests.get(
    'https://www.tekniskaverken.se/privat/avfall-och-atervinning/atervinningscentralerna/malmen/')

soup = bs4.BeautifulSoup(res.text, 'lxml')
for i in soup.select('.openinghours-status'):
    print(i.text)
    
    