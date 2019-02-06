"""
Course: cmps 4883
Assignemt: A03
Date: 02/06/2019
Github username: aanaree
Repo url: https://github.com/aanaree/4883-SWTools-greene
Name: Ackeem Greene
Description: 
        This progroms scrapes NFL gameddata from their website and used the data
        to extract the infomation and store it into a '.json' file
"""
from beautifulscraper import BeautifulScraper
from pprint import pprint
import urllib
import json
import sys
from time import sleep

scraper = BeautifulScraper()
delays = [.01,.02,.03,.04,.05]
pages = [x+1 for x in range(5)]

f = open("nfl_dat.json","w")

#used to change auto matically changed the years and weeks in each website
years = [x for x in range (2009,2019)]
weeks = [x for x in range (1,18)]

sREG = "REG"
sPOST = "POST"
#stores each game id
gameids =[]

#REGULAR SEASON STATS
for year in years:
        #gameids[year] = []
        for week in weeks:
                url = "http://www.nfl.com/schedules/%s/%s%s"%(year,sREG,str(week))
                page = scraper.go(url)

                #extracts the Game ID using the div from the nfl website
                divs = page.find_all('div',{"class":"schedules-list-content"})
                for div in divs:
                        gameids.append(div['data-gameid'])

#uses scraped game ID's to extract each games data and store it into a .json file
for gameid in gameids:
        url2 = "http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json"%(gameid,gameid)
        #stores the game data into the .json file
        urllib.request.urlretrieve(url2, 'nfl_json/'+gameid)


#POST SEASON STATS
for year in years:
        url = "http://www.nfl.com/schedules/%s/%s"%(year,sPOST)
        page = scraper.go(url)
        
        #extracts the Game ID using the div from the nfl website
        divs = page.find_all('div',{"class":"schedules-list-content"})
        for div in divs:
                gameids.append(div['data-gameid'])

#uses scraped game ID's to extract each games data and store it into a .json file
for gameid in gameids:
        url2 = "http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json"%(gameid,gameid)
        #stores the game data into the .json file
        urllib.request.urlretrieve(url2, 'nflp_json/'+gameid+'.json')
    
f.write(json.dumps(gameids))