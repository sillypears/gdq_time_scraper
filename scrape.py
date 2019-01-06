import os
import sys
#from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz
import time

URL = "https://gamesdonequick.com/schedule"
FILE = "agdq-2019-schedule-scrape.txt"
GAMES_FILE = "games-list.txt"
SLEEP_TIME = 60
tz = pytz.timezone("America/New_York")

def start_analysis(soup, games):
    tds = soup.find_all("td", {"class": "start-time text-right"})
    
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
        
        if setup_time and game_name in games:
            print("{} - {} by {}".format(start_time.astimezone(tz).strftime("%a @ %I:%M %p"), game_name, runner_name))

    print("")
    return 0
        
def main():
    os.system('cls')
    while(True):
        GAMES = []
        if os.path.exists(GAMES_FILE):
            with open(GAMES_FILE, "r") as f:
                GAMES.extend(f.read().split('\n'))
        else:
            GAMES = [
                "Overload",
                "Crypt of the NecroDancer: AMPLIFIED"
            ]
        if os.path.exists(FILE):
            with open(FILE, "r") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
        else:
            r = requests.get(URL)
            data = r.text
            soup = BeautifulSoup(data, "html.parser")
        os.system('cls')            
        print("Current Time: {}".format(datetime.now().strftime("%x %X")))
        start_analysis(soup, GAMES)
        time.sleep(SLEEP_TIME)

        

if __name__ == "__main__":
    sys.exit(main())
