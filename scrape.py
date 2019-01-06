
import os
import sys
#from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz

URL = "https://gamesdonequick.com/schedule"
FILE = "agdq-2018-schedule-scrape.txt"
GAMES = ("Overload", "Crypt of the NecroDancer: AMPLIFIED")
tz = pytz.timezone("America/New_York")

def start_analysis(soup):

    #print soup.prettify("utf-8")
    tds = soup.find_all("td", {"class": "start-time text-right"})
    print("game, setup")
    
    for td in tds:
        try: 
            
            start_time = pytz.utc.localize(datetime.fromisoformat(td.getText().strip()[:-1:]))
            
        except Exception as e:
            start_time = ""
            print(e)

        try: 
            game_name = td.findNextSibling().getText().strip()
        except:
            game_name = ""
        try: 
            runner_name = td.findNextSibling().findNextSibling().getText().strip()
        except: 
            runner_name = ""
        try:
            setup_time = td.findNextSibling().findNextSibling().findNextSibling().getText().strip()
        except:
            pass
        if setup_time and game_name in GAMES:
            print("{} - {} by {}".format(start_time.astimezone(tz), game_name, runner_name))
        


    # for td in tds:
    #     print(td)
    #     sys.exit()
    #     try:
    #         setup = td.getText().strip()
    #         game = td.findPreviousSibling().findPreviousSibling().getText().strip()
            
    #         if setup:
    #             print("{},{}".format(game, setup))
    #     except:
    #         pass


def main():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
    else:
        r = requests.get(URL)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")

    start_analysis(soup)

if __name__ == "__main__":
    sys.exit(main())
