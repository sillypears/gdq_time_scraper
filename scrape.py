import os
import sys
#from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz

URL = "https://gamesdonequick.com/schedule"
FILE = "agdq-2019-schedule-scrape.txt"
GAMES = ("Overload", "Crypt of the NecroDancer: AMPLIFIED")
tz = pytz.timezone("America/New_York")

def start_analysis(soup):
    tds = soup.find_all("td", {"class": "start-time text-right"})
    print("")
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
        
def main():
    while(True):
        if os.path.exists(FILE):
            with open(FILE, "r") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
        else:
            r = requests.get(URL)
            data = r.text
            soup = BeautifulSoup(data, "html.parser")
        
        start_analysis(soup)
        os.system("pause")

if __name__ == "__main__":
    sys.exit(main())
