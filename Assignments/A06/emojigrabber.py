"""
Course: cmps 4883
Assignemt: A06
Date: 03/11/2019
Github username: aanaree
Repo url: https://github.com/aanaree/4883-SWTools-greene
Name: Ackeem Greene
Description: 
        This progroms scrapes emoji from a website and stores the image in a folder
"""
from beautifulscraper import BeautifulScraper
from pprint import pprint
import urllib
import json
import sys
from time import sleep

scraper = BeautifulScraper()

f = open("emoji_data","w")

emoji_data = {}

x=1
url = "https://www.webfx.com/tools/emoji-cheat-sheet/"

page = scraper.go(url)

#go through website and grab each emoji location
for emoji in page.find_all("span",{"class":"emoji"}):
    image_path = emoji['data-src']
    #print(url+image_path)
    # save the image using requests library
    urllib.request.urlretrieve((url+image_path),"emojis/emoji%d.png"%(x))
    x+=1
    