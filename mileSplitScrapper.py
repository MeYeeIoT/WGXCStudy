from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import requests
import os

def linkAccepted(link):
    if(link.__contains__("Boys") or link.__contains__("BOYS") or link.__contains__("boys")):
        if(link.__contains__("II") or link.__contains__("Gold")):
            return True
        elif(link.__contains__("Varsity") and not(link.__contains__("Junior")) and not(link.__contains__("I"))):
            print("This should say false")
            print(not link.__contains__("Junior"))
            return True
        else:
            return False

site = "milesplit"
meetName = "/6231/perry-outdoor-family-center-xc-course"
dirName = "madison"
mileSplitName = "u-wanna-come-back"
startYear = 2021
endYear = 2023

def findMeets():
	teams = []
	request = Request("https://oh.milesplit.com/meets/501164-ohsaa-division-2-district-madison-2022/teams")
	page = urlopen(request)
	soup = BeautifulSoup(page, "lxml")
	for tag in soup.find_all("td", "name"):
			teams.append((tag.find("a")).get("href"))
	return teams

def main():
	if not os.path.exists(dirName):
		os.mkdir(dirName)
	findMeets()
if __name__=="__main__":
	main()
