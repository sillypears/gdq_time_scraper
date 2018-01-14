#!C:\Python27\python.exe

import os
import sys
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import requests

URL = "https://gamesdonequick.com/schedule"
FILE = "agdq-2018-schedule-scrape.txt"

def start_analysis(data_file):
    with open(data_file, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    #print soup.prettify("utf-8")
    tds = soup.find_all("td", {"class": "visible-lg text-center"})
    print "game, setup"
    for td in tds:
        try:
            setup = td.getText().strip()
            game = td.findPreviousSibling().findPreviousSibling().getText().strip()
            if setup:
                print "{},{}".format(game, setup)
        except:
            pass


def main():
    if os.path.exists(FILE):
        start_analysis(FILE)
    else:
        r = requests.get(URL)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        table = soup.find_all("table")[0]
        print len(table)
        with open(FILE, 'w') as f:
            f.write(table.prettify("utf-8"))

if __name__ == "__main__":
    sys.exit(main())
