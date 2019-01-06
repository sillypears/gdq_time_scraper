import os
import sys
#from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import pytz
import time
import json

URL = "https://gamesdonequick.com/schedule"
FILE = "agdq-2019-schedule-scrape.txt"
GAMES_FILE = "games-list.txt"
JSON_FILE = "agdq-2019-original-times.json"
SLEEP_TIME = 60
tz = pytz.timezone("America/New_York")

def start_analysis(soup, games, times):
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
        minutes_off_from_original = 0
        b_or_a = "later"
        if game_name in times.keys():
            og_time = datetime.fromisoformat(times[game_name])
            minutes_off_from_original = int((og_time - start_time).seconds % 3600/60)
            #print("{} - {} = {}".format(og_time, start_time,  int((og_time - start_time).seconds % 3600/60)))
        if minutes_off_from_original < 0:
            b_or_a = "faster"
        if setup_time and game_name in games:
            print("{} - {} by {} _ {} min {}".format(start_time.astimezone(tz).strftime("%a @ %I:%M %p"), game_name, runner_name, minutes_off_from_original, b_or_a))

    print("")
    return 0
        
def main():
    os.system('cls')
    times = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            times = json.loads(f.read())
    
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
        start_analysis(soup, GAMES, times)
        time.sleep(SLEEP_TIME)

        

if __name__ == "__main__":
    sys.exit(main())
