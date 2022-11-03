from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import requests
import os
from time import sleep
class ListTooLong(Exception):
	pass
def linkAccepted(link):
    if(link.__contains__("Valley")) or (link.__contains__("Open")) or (link.__contains__("2500")) or (link.__contains__("2.15")):
        return False
    if(link.__contains__("Boys") or link.__contains__("BOYS") or link.__contains__("boys")):
        if(link.__contains__("II") or link.__contains__("Gold")) or link.__contains__("2"):
            return True
        elif(link.__contains__("Varsity") and not(link.__contains__("Junior")) and not(link.__contains__("I")) and not(link.__contains__("1")) and not(link.__contains__("MS")) and not link.__contains__("Red")):
            return True
        elif(link.__contains__("High School Boys") and not(link.__contains__("1"))):
            return True
        else:
            return False
    elif(link.__contains__("Division 2 Results") or link.__contains__("Varsity D2/3 Results") or link.__contains__("Blue") and not(link.__contains__("1")) and not(link.__contains__("3")) and not(link.__contains__("Boys")) and not(link.__contains__("Girls")) and not(link.__contains__("MS"))):
        return True
    elif(link.__contains__("Blue") and link.__contains__("Boys") and not(link.__contains__("MS"))):
        return True
    elif(link.__contains__("\"Completed\" Results")):
        return True
def getTeams():
	teams = []
	request = Request("https://oh.milesplit.com/meets/501164-ohsaa-division-2-district-madison-2022/teams")
	page = urlopen(request)
	soup = BeautifulSoup(page, "lxml")
	for tag in soup.find_all("td", "name"):
			urlString = str(tag.find("a").get("href"))
			teamNumber = [int(x) for x in urlString if x.isdigit()]
			cNum = ""
			for n in teamNumber:
				cNum+=str(n)
			teams.append(int(cNum))
	return teams
def getMeets(team, year):
	meetsData = []
	response = requests.get("https://oh.milesplit.com/api/v1/teams/"+str(team)+"/schedules?season=cc&year="+str(year))
	meetData = response.json()
	for x in meetData["data"]:
		for y in range(len(meetData["data"][x])):
			for d in range(len(meetData["data"][x][y]["items"])):
				name = meetData["data"][x][y]["items"][d]["name"]
				meetLink = meetData["data"][x][y]["items"][d]["link"]
				meetsData.append([name, meetLink])
	return meetsData
def getMeetResults(meetData, year):
	name = (meetData[0]).lower()
	name = name.replace(" - ", " ")
	name = name.replace(" ", "-")
	meetLink = meetData[1]+"-"+name+"-"+str(year)+"/results"
	resultsRequest = Request(meetLink)
	resultPage = urlopen(resultsRequest)
	resultSoup = BeautifulSoup(resultPage, "lxml")
	raceLink = None
	results = None
	date = None
	for link in resultSoup.findAll("a"):
		currentLink = link.get("href")
		try:
			linkText = link.contents[0]
		except:
			continue
		if(currentLink.__contains__("https://www.milesplit")):
			continue
		if linkAccepted(linkText):
			if (currentLink.__contains__("/raw")):
				raceLink = currentLink
			else:
				raceLink = currentLink + "/raw"
	if raceLink is not None:
		resultsRequest = Request(raceLink)
		resultsPage = urlopen(resultsRequest)
		resultSoup = BeautifulSoup(resultsPage, "lxml")
		date = resultSoup.find("time").text.strip()
		location = resultSoup.find("div", "venueCity").text.strip()
		results = str(resultSoup.find("div", id="meetResultsBody"))
	times = []
	lines = results.split("\n")
	try:
		for line in lines:
			if (line.__contains__("West Geauga")):
				for item in line.split():
					if (item.__contains__(":") and int(item.split(":")[0])>12 and int(item.split(":")[0])<45):
						if (len(times)>=7):
							raise ListTooLong
						else:
							times.append(item)
	except ListTooLong:
		pass
	return {meetData[0]:[times, date, location]}
def main():
	startYear = 2021
	endYear = 2022
	results = []
	teams = getTeams()
	#for team in teams:
	team = 9454
	year = 2021
	#for year in range(startYear, endYear):
	meets = getMeets(team, year)
	yearResults = []
	for meet in meets:
		results = getMeetResults(meet, year)
		yearResults.append(results)
	print(yearResults)
if __name__=="__main__":
	main()
